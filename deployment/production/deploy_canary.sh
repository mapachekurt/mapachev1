#!/bin/bash
# Canary Deployment Script for Production
# Gradually routes traffic with quality gates and auto-rollback

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="agent-improvements-prod"
LOG_FILE="/tmp/canary-deploy-$(date +%Y%m%d-%H%M%S).log"

# Canary stages with monitoring duration (in seconds)
declare -A CANARY_STAGES=(
    [1]=300      # 1% for 5 minutes
    [10]=300     # 10% for 5 minutes
    [25]=300     # 25% for 5 minutes
    [50]=300     # 50% for 5 minutes
    [100]=600    # 100% for 10 minutes
)

# Metrics thresholds and quality gates
SUCCESS_RATE_THRESHOLD=0.99
ERROR_RATE_THRESHOLD=0.01
P95_LATENCY_THRESHOLD=5000
COST_DEVIATION_THRESHOLD=0.20
MIN_REQUEST_SAMPLE=100  # Minimum requests before making decisions

# Baseline metrics (populated during deployment)
declare -A BASELINE_METRICS

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_canary() {
    echo -e "${MAGENTA}[CANARY]${NC} $1" | tee -a "$LOG_FILE"
}

log_gate() {
    echo -e "${CYAN}[GATE]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to require confirmation
require_confirmation() {
    local action="$1"
    echo ""
    log_warn "⚠️  PRODUCTION CANARY DEPLOYMENT: $action"
    log_warn "Project: $PROJECT_ID"
    log_warn "Service: $SERVICE_NAME"
    log_warn "Strategy: 1% → 10% → 25% → 50% → 100%"
    echo ""
    read -p "Are you sure you want to proceed? (type 'yes' to confirm): " confirmation

    if [ "$confirmation" != "yes" ]; then
        log_error "Canary deployment cancelled by user"
        exit 1
    fi
    log_info "Confirmation received, proceeding..."
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."

    if [ -z "$PROJECT_ID" ]; then
        log_error "GCP_PROJECT_ID environment variable not set"
        exit 1
    fi

    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI not found"
        exit 1
    fi

    if ! command -v bc &> /dev/null; then
        log_error "bc not found (required for calculations)"
        exit 1
    fi

    # Verify git repository is clean
    if ! git diff-index --quiet HEAD --; then
        log_error "Working directory has uncommitted changes"
        exit 1
    fi

    log_info "Prerequisites check passed ✓"
}

# Get current stable revision
get_stable_revision() {
    log_step "Identifying current stable revision..."

    STABLE_REVISION=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.latestReadyRevisionName)")

    if [ -z "$STABLE_REVISION" ]; then
        log_error "Could not determine stable revision"
        exit 1
    fi

    log_info "Stable revision: $STABLE_REVISION"
}

# Collect baseline metrics
collect_baseline_metrics() {
    log_step "Collecting baseline metrics from stable revision..."

    # Get baseline error rate
    local errors=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${STABLE_REVISION} AND metric.type=run.googleapis.com/request_count AND metric.labels.response_code_class=5xx" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    local total=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${STABLE_REVISION} AND metric.type=run.googleapis.com/request_count" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "1")

    BASELINE_METRICS[error_rate]=$(echo "scale=6; $errors / $total" | bc)
    BASELINE_METRICS[success_rate]=$(echo "scale=6; 1 - ${BASELINE_METRICS[error_rate]}" | bc)

    # Get baseline P95 latency
    BASELINE_METRICS[p95_latency]=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${STABLE_REVISION} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[95])" \
        --limit=1 2>/dev/null || echo "1000")

    log_info "Baseline metrics collected:"
    log_info "  Success rate: ${BASELINE_METRICS[success_rate]}"
    log_info "  Error rate: ${BASELINE_METRICS[error_rate]}"
    log_info "  P95 latency: ${BASELINE_METRICS[p95_latency]}ms"
}

# Build canary image
build_canary_image() {
    log_step "Building canary container image..."

    GIT_SHA=$(git rev-parse --short HEAD)
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    CANARY_TAG="canary-${GIT_SHA}-${TIMESTAMP}"

    log_info "Git SHA: $GIT_SHA"
    log_info "Canary tag: $CANARY_TAG"

    gcloud builds submit \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${CANARY_TAG}" \
        --project="$PROJECT_ID" \
        . | tee -a "$LOG_FILE"

    CANARY_IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${CANARY_TAG}"
    log_success "Canary image built: $CANARY_IMAGE"
}

# Deploy canary revision (no traffic initially)
deploy_canary_revision() {
    log_step "Deploying canary revision (0% traffic)..."

    local sa_email="agent-production@${PROJECT_ID}.iam.gserviceaccount.com"
    CANARY_REVISION="${SERVICE_NAME}-canary-${TIMESTAMP}"

    log_canary "Deploying revision: $CANARY_REVISION"
    log_canary "Image: $CANARY_IMAGE"

    gcloud run deploy "$SERVICE_NAME" \
        --image="$CANARY_IMAGE" \
        --platform=managed \
        --region="$REGION" \
        --service-account="$sa_email" \
        --memory=4Gi \
        --cpu=4 \
        --timeout=300 \
        --concurrency=80 \
        --min-instances=1 \
        --max-instances=10 \
        --set-env-vars="ENVIRONMENT=production,LOG_LEVEL=INFO,GCP_PROJECT_ID=${PROJECT_ID},DEPLOYMENT_TYPE=canary" \
        --set-secrets="REDIS_URL=redis-url-prod:latest,PRODUCTION_CONFIG=production-config:latest" \
        --no-allow-unauthenticated \
        --project="$PROJECT_ID" \
        --tag="canary" \
        --no-traffic \
        --revision-suffix="canary-${TIMESTAMP}" | tee -a "$LOG_FILE"

    # Get canary URL for testing
    CANARY_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.traffic.tag[canary].url)")

    log_success "Canary revision deployed: $CANARY_URL"
}

# Run smoke tests on canary
run_canary_smoke_tests() {
    log_step "Running smoke tests on canary revision..."

    local tests_passed=true

    # Test 1: Health check
    log_info "Test 1: Health check..."
    if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
        "${CANARY_URL}/health" | grep -q "healthy"; then
        log_success "✓ Health check passed"
    else
        log_error "✗ Health check failed"
        tests_passed=false
    fi

    # Test 2: Readiness
    log_info "Test 2: Readiness check..."
    if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
        "${CANARY_URL}/ready" | grep -q "ready"; then
        log_success "✓ Readiness check passed"
    else
        log_error "✗ Readiness check failed"
        tests_passed=false
    fi

    # Test 3: Redis connectivity
    log_info "Test 3: Redis connectivity..."
    if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
        "${CANARY_URL}/health/redis" | grep -q "connected"; then
        log_success "✓ Redis connectivity verified"
    else
        log_error "✗ Redis connectivity failed"
        tests_passed=false
    fi

    if [ "$tests_passed" = false ]; then
        log_error "Smoke tests failed, aborting canary deployment"
        cleanup_canary
        exit 1
    fi

    log_success "All smoke tests passed ✓"
}

# Progressive traffic shift with quality gates
progressive_traffic_shift() {
    log_step "Starting progressive traffic shift..."

    for percentage in 1 10 25 50 100; do
        local duration=${CANARY_STAGES[$percentage]}
        local stable_percentage=$((100 - percentage))

        log_canary "=========================================="
        log_canary "CANARY STAGE: ${percentage}% traffic"
        log_canary "Duration: ${duration}s ($(($duration / 60)) minutes)"
        log_canary "=========================================="

        # Update traffic split
        if [ $percentage -eq 100 ]; then
            gcloud run services update-traffic "$SERVICE_NAME" \
                --region="$REGION" \
                --project="$PROJECT_ID" \
                --to-revisions="${CANARY_REVISION}=100" | tee -a "$LOG_FILE"
        else
            gcloud run services update-traffic "$SERVICE_NAME" \
                --region="$REGION" \
                --project="$PROJECT_ID" \
                --to-revisions="${CANARY_REVISION}=${percentage},${STABLE_REVISION}=${stable_percentage}" | tee -a "$LOG_FILE"
        fi

        log_success "Traffic shifted: ${percentage}% canary, ${stable_percentage}% stable"

        # Monitor this stage
        monitor_canary_stage "$percentage" "$duration"

        # Quality gate check
        if ! quality_gate_check "$percentage"; then
            log_error "Quality gate failed at ${percentage}% stage"
            log_error "Initiating automatic rollback..."
            rollback_canary
            exit 1
        fi

        log_success "Stage ${percentage}% complete - quality gates passed ✓"
    done

    log_success "Progressive traffic shift complete ✓"
}

# Monitor canary at specific stage
monitor_canary_stage() {
    local percentage="$1"
    local duration="$2"
    local check_interval=60  # Check every minute
    local checks=$((duration / check_interval))

    log_info "Monitoring ${percentage}% stage for ${duration}s..."

    for ((i=1; i<=checks; i++)); do
        local elapsed=$((i * check_interval))
        log_info "Stage ${percentage}% - Progress: ${elapsed}s / ${duration}s"

        # Get canary metrics
        get_canary_metrics "$percentage"

        # Check for immediate failures
        if (( $(echo "${CANARY_METRICS[error_rate]} > 0.05" | bc -l) )); then
            log_error "Critical error rate detected: ${CANARY_METRICS[error_rate]}"
            return 1
        fi

        if [ $i -lt $checks ]; then
            sleep $check_interval
        fi
    done

    log_info "Monitoring complete for ${percentage}% stage"
}

# Get canary-specific metrics
get_canary_metrics() {
    local percentage="$1"

    # Get canary error rate
    local errors=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${CANARY_REVISION} AND metric.type=run.googleapis.com/request_count AND metric.labels.response_code_class=5xx" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    local total=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${CANARY_REVISION} AND metric.type=run.googleapis.com/request_count" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "1")

    CANARY_METRICS[error_rate]=$(echo "scale=6; $errors / $total" | bc)
    CANARY_METRICS[success_rate]=$(echo "scale=6; 1 - ${CANARY_METRICS[error_rate]}" | bc)
    CANARY_METRICS[request_count]=$total

    # Get canary P95 latency
    CANARY_METRICS[p95_latency]=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND resource.labels.revision_name=${CANARY_REVISION} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[95])" \
        --limit=1 2>/dev/null || echo "0")

    log_info "Canary metrics (${percentage}%):"
    log_info "  Requests: ${CANARY_METRICS[request_count]}"
    log_info "  Success rate: ${CANARY_METRICS[success_rate]}"
    log_info "  Error rate: ${CANARY_METRICS[error_rate]}"
    log_info "  P95 latency: ${CANARY_METRICS[p95_latency]}ms"
}

# Quality gate check
quality_gate_check() {
    local percentage="$1"
    log_gate "Running quality gate checks for ${percentage}% stage..."

    local gate_passed=true

    # Gate 1: Minimum request sample
    if (( ${CANARY_METRICS[request_count]:-0} < MIN_REQUEST_SAMPLE )); then
        log_warn "Insufficient sample size: ${CANARY_METRICS[request_count]} < $MIN_REQUEST_SAMPLE"
        log_warn "Accepting stage but consider extending monitoring"
    fi

    # Gate 2: Success rate threshold
    if (( $(echo "${CANARY_METRICS[success_rate]} < $SUCCESS_RATE_THRESHOLD" | bc -l) )); then
        log_error "✗ Gate 2 FAILED: Success rate ${CANARY_METRICS[success_rate]} < $SUCCESS_RATE_THRESHOLD"
        gate_passed=false
    else
        log_success "✓ Gate 2 PASSED: Success rate ${CANARY_METRICS[success_rate]} >= $SUCCESS_RATE_THRESHOLD"
    fi

    # Gate 3: Error rate threshold
    if (( $(echo "${CANARY_METRICS[error_rate]} > $ERROR_RATE_THRESHOLD" | bc -l) )); then
        log_error "✗ Gate 3 FAILED: Error rate ${CANARY_METRICS[error_rate]} > $ERROR_RATE_THRESHOLD"
        gate_passed=false
    else
        log_success "✓ Gate 3 PASSED: Error rate ${CANARY_METRICS[error_rate]} <= $ERROR_RATE_THRESHOLD"
    fi

    # Gate 4: P95 latency threshold
    if (( $(echo "${CANARY_METRICS[p95_latency]} > $P95_LATENCY_THRESHOLD" | bc -l) )); then
        log_error "✗ Gate 4 FAILED: P95 latency ${CANARY_METRICS[p95_latency]}ms > ${P95_LATENCY_THRESHOLD}ms"
        gate_passed=false
    else
        log_success "✓ Gate 4 PASSED: P95 latency ${CANARY_METRICS[p95_latency]}ms <= ${P95_LATENCY_THRESHOLD}ms"
    fi

    # Gate 5: Compare to baseline
    local latency_increase=$(echo "scale=4; ${CANARY_METRICS[p95_latency]} / ${BASELINE_METRICS[p95_latency]}" | bc)
    if (( $(echo "$latency_increase > 1.5" | bc -l) )); then
        log_error "✗ Gate 5 FAILED: Latency increased by $(echo "scale=0; ($latency_increase - 1) * 100" | bc)% vs baseline"
        gate_passed=false
    else
        log_success "✓ Gate 5 PASSED: Latency within acceptable range of baseline"
    fi

    if [ "$gate_passed" = true ]; then
        log_success "All quality gates passed for ${percentage}% stage ✓"
        return 0
    else
        log_error "Quality gates failed for ${percentage}% stage ✗"
        return 1
    fi
}

# Rollback canary deployment
rollback_canary() {
    log_error "=========================================="
    log_error "  ROLLING BACK CANARY DEPLOYMENT"
    log_error "=========================================="

    # Shift all traffic back to stable
    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${STABLE_REVISION}=100" | tee -a "$LOG_FILE"

    log_success "Rollback complete - 100% traffic on stable revision"

    # Cleanup canary revision
    cleanup_canary

    send_alert "CANARY_ROLLBACK" "Canary deployment rolled back due to quality gate failure"
}

# Cleanup canary revision
cleanup_canary() {
    log_step "Cleaning up canary revision..."

    gcloud run revisions delete "$CANARY_REVISION" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --quiet 2>/dev/null || log_warn "Could not delete canary revision"

    log_info "Canary revision cleaned up"
}

# Send alert notification
send_alert() {
    local alert_type="$1"
    local message="$2"

    log_warn "ALERT: $alert_type - $message"

    gcloud logging write canary-deployment \
        "{\"alert_type\": \"$alert_type\", \"message\": \"$message\", \"service\": \"$SERVICE_NAME\"}" \
        --severity=ERROR \
        --project="$PROJECT_ID" 2>/dev/null || true

    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"🐤 $alert_type: $message\"}" 2>/dev/null || true
    fi
}

# Generate deployment report
generate_report() {
    log_step "Generating canary deployment report..."

    cat > "/tmp/canary-report-${TIMESTAMP}.txt" << EOF
===============================================
CANARY DEPLOYMENT REPORT
===============================================

Timestamp: $(date)
Project: $PROJECT_ID
Region: $REGION
Service: $SERVICE_NAME

DEPLOYMENT DETAILS:
-------------------
Git SHA: $GIT_SHA
Stable Revision: $STABLE_REVISION
Canary Revision: $CANARY_REVISION
Canary Image: $CANARY_IMAGE

DEPLOYMENT STATUS: SUCCESS
Final Traffic: 100% on canary

CANARY STAGES:
--------------
Stage 1:   1% traffic - PASSED
Stage 2:  10% traffic - PASSED
Stage 3:  25% traffic - PASSED
Stage 4:  50% traffic - PASSED
Stage 5: 100% traffic - PASSED

BASELINE METRICS:
-----------------
Success Rate: ${BASELINE_METRICS[success_rate]}
Error Rate: ${BASELINE_METRICS[error_rate]}
P95 Latency: ${BASELINE_METRICS[p95_latency]}ms

FINAL CANARY METRICS:
---------------------
Success Rate: ${CANARY_METRICS[success_rate]}
Error Rate: ${CANARY_METRICS[error_rate]}
P95 Latency: ${CANARY_METRICS[p95_latency]}ms

QUALITY GATES:
--------------
All stages passed quality gates
No rollback required

LOG FILE: $LOG_FILE

===============================================
EOF

    log_info "Report saved: /tmp/canary-report-${TIMESTAMP}.txt"
    cat "/tmp/canary-report-${TIMESTAMP}.txt"
}

# Main execution
main() {
    log_info "=========================================="
    log_info "  CANARY PRODUCTION DEPLOYMENT"
    log_info "=========================================="
    log_info ""
    log_info "Log file: $LOG_FILE"
    log_info "Strategy: 1% → 10% → 25% → 50% → 100%"
    log_info ""

    require_confirmation "Canary deployment to production"

    check_prerequisites
    get_stable_revision
    collect_baseline_metrics
    build_canary_image
    deploy_canary_revision
    run_canary_smoke_tests
    progressive_traffic_shift
    generate_report

    log_success ""
    log_success "=========================================="
    log_success "  CANARY DEPLOYMENT COMPLETE ✓"
    log_success "=========================================="
    log_success ""
    log_success "New version is live with 100% traffic"
    log_success "All quality gates passed"
    log_success ""
}

# Run main function
main "$@"
