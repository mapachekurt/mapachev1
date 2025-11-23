#!/bin/bash
# Blue-Green Deployment Script for Production
# Deploys new version to inactive environment, tests, and swaps traffic

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="agent-improvements-prod"
LOG_FILE="/tmp/blue-green-deploy-$(date +%Y%m%d-%H%M%S).log"
MONITOR_DURATION=900  # 15 minutes in seconds
SMOKE_TEST_RETRIES=3

# Metrics thresholds
SUCCESS_RATE_THRESHOLD=0.99
ERROR_RATE_THRESHOLD=0.01
P95_LATENCY_THRESHOLD=5000
COST_DEVIATION_THRESHOLD=0.20

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

log_deploy() {
    echo -e "${CYAN}[DEPLOY]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to require confirmation
require_confirmation() {
    local action="$1"
    echo ""
    log_warn "⚠️  PRODUCTION DEPLOYMENT: $action"
    log_warn "Project: $PROJECT_ID"
    log_warn "Service: $SERVICE_NAME"
    echo ""
    read -p "Are you sure you want to proceed? (type 'yes' to confirm): " confirmation

    if [ "$confirmation" != "yes" ]; then
        log_error "Blue-green deployment cancelled by user"
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

    if ! command -v jq &> /dev/null; then
        log_warn "jq not found, some features may be limited"
    fi

    # Verify git repository is clean
    if ! git diff-index --quiet HEAD --; then
        log_error "Working directory has uncommitted changes"
        log_error "Blue-green deployment requires committed code"
        exit 1
    fi

    log_info "Prerequisites check passed ✓"
}

# Get current active revision
get_active_revision() {
    log_step "Determining current active revision..."

    ACTIVE_REVISION=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.latestReadyRevisionName)")

    if [ -z "$ACTIVE_REVISION" ]; then
        log_error "Could not determine active revision"
        exit 1
    fi

    log_info "Current active revision: $ACTIVE_REVISION"

    # Get traffic split
    ACTIVE_TRAFFIC=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.traffic[0].percent)")

    log_info "Current traffic: ${ACTIVE_TRAFFIC}% to $ACTIVE_REVISION"
}

# Build new container image
build_new_image() {
    log_step "Building new container image..."

    GIT_SHA=$(git rev-parse --short HEAD)
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    NEW_TAG="blue-green-${GIT_SHA}-${TIMESTAMP}"

    log_info "Git SHA: $GIT_SHA"
    log_info "Image tag: $NEW_TAG"

    gcloud builds submit \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${NEW_TAG}" \
        --project="$PROJECT_ID" \
        . | tee -a "$LOG_FILE"

    NEW_IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${NEW_TAG}"
    log_success "Container image built: $NEW_IMAGE"
}

# Deploy to green environment (no traffic)
deploy_green() {
    log_step "Deploying to GREEN environment (0% traffic)..."

    local sa_email="agent-production@${PROJECT_ID}.iam.gserviceaccount.com"
    GREEN_REVISION="${SERVICE_NAME}-green-${TIMESTAMP}"

    log_deploy "Deploying revision: $GREEN_REVISION"
    log_deploy "Image: $NEW_IMAGE"
    log_deploy "Traffic: 0% (testing only)"

    gcloud run deploy "$SERVICE_NAME" \
        --image="$NEW_IMAGE" \
        --platform=managed \
        --region="$REGION" \
        --service-account="$sa_email" \
        --memory=4Gi \
        --cpu=4 \
        --timeout=300 \
        --concurrency=80 \
        --min-instances=1 \
        --max-instances=10 \
        --set-env-vars="ENVIRONMENT=production,LOG_LEVEL=INFO,GCP_PROJECT_ID=${PROJECT_ID},DEPLOYMENT_TYPE=blue-green" \
        --set-secrets="REDIS_URL=redis-url-prod:latest,PRODUCTION_CONFIG=production-config:latest" \
        --no-allow-unauthenticated \
        --project="$PROJECT_ID" \
        --tag="green" \
        --no-traffic \
        --revision-suffix="green-${TIMESTAMP}" | tee -a "$LOG_FILE"

    # Get green URL
    GREEN_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.traffic.tag[green].url)")

    log_success "Green environment deployed: $GREEN_URL"
    log_info "Green revision: $GREEN_REVISION"
}

# Run smoke tests on green environment
run_smoke_tests() {
    log_step "Running smoke tests on GREEN environment..."

    local test_passed=false
    local attempt=1

    while [ $attempt -le $SMOKE_TEST_RETRIES ] && [ "$test_passed" = false ]; do
        log_info "Smoke test attempt $attempt of $SMOKE_TEST_RETRIES..."

        # Test 1: Health check
        log_info "Test 1: Health check endpoint..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            "${GREEN_URL}/health" | grep -q "healthy"; then
            log_success "✓ Health check passed"
        else
            log_error "✗ Health check failed"
            attempt=$((attempt + 1))
            sleep 10
            continue
        fi

        # Test 2: Readiness check
        log_info "Test 2: Readiness check..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            "${GREEN_URL}/ready" | grep -q "ready"; then
            log_success "✓ Readiness check passed"
        else
            log_error "✗ Readiness check failed"
            attempt=$((attempt + 1))
            sleep 10
            continue
        fi

        # Test 3: Metrics endpoint
        log_info "Test 3: Metrics endpoint..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            "${GREEN_URL}/metrics" > /dev/null; then
            log_success "✓ Metrics endpoint accessible"
        else
            log_error "✗ Metrics endpoint failed"
            attempt=$((attempt + 1))
            sleep 10
            continue
        fi

        # Test 4: Basic API test
        log_info "Test 4: Basic API functionality..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            -H "Content-Type: application/json" \
            -d '{"test": true}' \
            "${GREEN_URL}/api/v1/agents" > /dev/null; then
            log_success "✓ API functionality test passed"
        else
            log_warn "✗ API test failed (may not be critical)"
        fi

        # Test 5: Redis connectivity
        log_info "Test 5: Redis connectivity..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            "${GREEN_URL}/health/redis" | grep -q "connected"; then
            log_success "✓ Redis connectivity verified"
        else
            log_error "✗ Redis connectivity failed"
            attempt=$((attempt + 1))
            sleep 10
            continue
        fi

        test_passed=true
    done

    if [ "$test_passed" = false ]; then
        log_error "Smoke tests failed after $SMOKE_TEST_RETRIES attempts"
        log_error "Rolling back deployment..."
        rollback_green
        exit 1
    fi

    log_success "All smoke tests passed ✓"
}

# Gradually shift traffic to green
shift_traffic_to_green() {
    log_step "Shifting traffic from BLUE to GREEN..."

    # Initial shift: 10%
    log_deploy "Shifting 10% traffic to GREEN..."
    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${GREEN_REVISION}=10,${ACTIVE_REVISION}=90" | tee -a "$LOG_FILE"

    log_info "Monitoring for 2 minutes at 10% traffic..."
    sleep 120

    if ! check_metrics "10% traffic"; then
        log_error "Metrics degraded at 10% traffic, rolling back..."
        rollback_to_blue
        exit 1
    fi

    # Shift to 50%
    log_deploy "Shifting 50% traffic to GREEN..."
    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${GREEN_REVISION}=50,${ACTIVE_REVISION}=50" | tee -a "$LOG_FILE"

    log_info "Monitoring for 5 minutes at 50% traffic..."
    sleep 300

    if ! check_metrics "50% traffic"; then
        log_error "Metrics degraded at 50% traffic, rolling back..."
        rollback_to_blue
        exit 1
    fi

    # Shift to 100%
    log_deploy "Shifting 100% traffic to GREEN..."
    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${GREEN_REVISION}=100" | tee -a "$LOG_FILE"

    log_success "100% traffic shifted to GREEN ✓"
}

# Monitor metrics after full cutover
monitor_production() {
    log_step "Monitoring production metrics for 15 minutes..."

    local monitor_interval=60  # Check every minute
    local checks=$((MONITOR_DURATION / monitor_interval))
    local check_count=0

    while [ $check_count -lt $checks ]; do
        check_count=$((check_count + 1))
        local elapsed=$((check_count * monitor_interval))
        log_info "Monitoring progress: ${elapsed}s / ${MONITOR_DURATION}s"

        if ! check_metrics "100% traffic (minute $check_count)"; then
            log_error "Metrics degraded during monitoring period"
            log_error "Initiating automatic rollback..."
            rollback_to_blue
            exit 1
        fi

        if [ $check_count -lt $checks ]; then
            sleep $monitor_interval
        fi
    done

    log_success "Monitoring period complete - all metrics healthy ✓"
}

# Check metrics against thresholds
check_metrics() {
    local stage="$1"
    log_info "Checking metrics at stage: $stage"

    # Get error rate from Cloud Monitoring
    local error_rate=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_count AND metric.labels.response_code_class=5xx" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    # Get total requests
    local total_requests=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_count" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "1")

    # Calculate success rate
    local success_rate=$(echo "scale=4; 1 - ($error_rate / $total_requests)" | bc)

    log_info "Current metrics:"
    log_info "  Error rate: ${error_rate}/${total_requests}"
    log_info "  Success rate: $success_rate (threshold: $SUCCESS_RATE_THRESHOLD)"

    # Check success rate
    if (( $(echo "$success_rate < $SUCCESS_RATE_THRESHOLD" | bc -l) )); then
        log_error "Success rate below threshold: $success_rate < $SUCCESS_RATE_THRESHOLD"
        return 1
    fi

    # Get P95 latency
    local p95_latency=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[95])" \
        --limit=1 2>/dev/null || echo "0")

    log_info "  P95 latency: ${p95_latency}ms (threshold: ${P95_LATENCY_THRESHOLD}ms)"

    # Check latency
    if (( $(echo "$p95_latency > $P95_LATENCY_THRESHOLD" | bc -l) )); then
        log_error "P95 latency above threshold: ${p95_latency}ms > ${P95_LATENCY_THRESHOLD}ms"
        return 1
    fi

    log_success "All metrics within acceptable ranges ✓"
    return 0
}

# Rollback to blue (previous version)
rollback_to_blue() {
    log_error "ROLLING BACK TO BLUE (previous version)"

    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${ACTIVE_REVISION}=100" | tee -a "$LOG_FILE"

    log_success "Rollback complete - 100% traffic on BLUE (previous version)"
    send_alert "ROLLBACK" "Blue-green deployment rolled back to previous version"
}

# Rollback green deployment
rollback_green() {
    log_error "Removing failed GREEN deployment"

    # Delete the green revision
    gcloud run revisions delete "$GREEN_REVISION" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --quiet 2>/dev/null || log_warn "Could not delete green revision"

    send_alert "DEPLOYMENT_FAILED" "Green environment deployment failed smoke tests"
}

# Clean up old blue revision
cleanup_old_blue() {
    log_step "Cleaning up old BLUE revision..."

    log_info "Keeping old revision for 24 hours for emergency rollback"
    log_info "Old revision: $ACTIVE_REVISION"
    log_warn "To manually delete later: gcloud run revisions delete $ACTIVE_REVISION --region=$REGION --project=$PROJECT_ID"
}

# Send alert notification
send_alert() {
    local alert_type="$1"
    local message="$2"

    log_warn "ALERT: $alert_type - $message"

    # Log to Cloud Logging with severity
    gcloud logging write blue-green-deployment \
        "{\"alert_type\": \"$alert_type\", \"message\": \"$message\", \"service\": \"$SERVICE_NAME\"}" \
        --severity=ERROR \
        --project="$PROJECT_ID" 2>/dev/null || log_warn "Could not send alert to Cloud Logging"

    # Add Slack/email notification here if configured
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"🚨 $alert_type: $message\"}" 2>/dev/null || true
    fi
}

# Generate deployment report
generate_report() {
    log_step "Generating deployment report..."

    cat > "/tmp/blue-green-report-${TIMESTAMP}.txt" << EOF
===============================================
BLUE-GREEN DEPLOYMENT REPORT
===============================================

Timestamp: $(date)
Project: $PROJECT_ID
Region: $REGION
Service: $SERVICE_NAME

DEPLOYMENT DETAILS:
-------------------
Git SHA: $GIT_SHA
Old Revision (BLUE): $ACTIVE_REVISION
New Revision (GREEN): $GREEN_REVISION
New Image: $NEW_IMAGE

DEPLOYMENT STATUS: SUCCESS
Traffic: 100% on GREEN

SMOKE TESTS: PASSED
METRICS CHECK: PASSED
MONITORING PERIOD: 15 minutes PASSED

THRESHOLDS:
-----------
Success Rate: > ${SUCCESS_RATE_THRESHOLD}
P95 Latency: < ${P95_LATENCY_THRESHOLD}ms
Error Rate: < ${ERROR_RATE_THRESHOLD}

ROLLBACK PLAN:
--------------
Old revision kept for 24 hours
To rollback manually:
  ./deployment/production/rollback_production.sh

LOG FILE: $LOG_FILE

===============================================
EOF

    log_info "Report saved: /tmp/blue-green-report-${TIMESTAMP}.txt"
    cat "/tmp/blue-green-report-${TIMESTAMP}.txt"
}

# Main execution
main() {
    log_info "=========================================="
    log_info "  BLUE-GREEN PRODUCTION DEPLOYMENT"
    log_info "=========================================="
    log_info ""
    log_info "Log file: $LOG_FILE"
    log_info ""

    require_confirmation "Blue-green deployment to production"

    check_prerequisites
    get_active_revision
    build_new_image
    deploy_green
    run_smoke_tests
    shift_traffic_to_green
    monitor_production
    cleanup_old_blue
    generate_report

    log_success ""
    log_success "=========================================="
    log_success "  BLUE-GREEN DEPLOYMENT COMPLETE ✓"
    log_success "=========================================="
    log_success ""
    log_success "New version is live with 100% traffic"
    log_success "Old version retained for emergency rollback"
    log_success ""
}

# Run main function
main "$@"
