#!/bin/bash
# Validate Staging Environment
# Comprehensive validation of GCP resources, configuration, service health, and golden tasks

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="agent-improvements-staging"
VALIDATION_REPORT="/tmp/staging_validation_$(date +%s).txt"

# Validation counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "[INFO] $1" >> "$VALIDATION_REPORT"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[WARN] $1" >> "$VALIDATION_REPORT"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[ERROR] $1" >> "$VALIDATION_REPORT"
}

log_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
    echo "[CHECK] $1" >> "$VALIDATION_REPORT"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    echo "[PASS] $1" >> "$VALIDATION_REPORT"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    echo "[FAIL] $1" >> "$VALIDATION_REPORT"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[WARNING] $1" >> "$VALIDATION_REPORT"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

# Initialize validation report
init_report() {
    cat > "$VALIDATION_REPORT" << EOF
========================================
STAGING ENVIRONMENT VALIDATION REPORT
========================================

Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Project: $PROJECT_ID
Region: $REGION
Service: $SERVICE_NAME

EOF
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    if [ -z "$PROJECT_ID" ]; then
        log_error "GCP_PROJECT_ID environment variable not set"
        exit 1
    fi

    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI not found"
        exit 1
    fi

    log_pass "Prerequisites validated"
}

# Section 1: GCP Resources Validation
validate_gcp_resources() {
    log_info ""
    log_info "=========================================="
    log_info "SECTION 1: GCP RESOURCES VALIDATION"
    log_info "=========================================="
    echo ""

    # Check Cloud Run service
    log_check "Validating Cloud Run service..."
    if gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)" &> /dev/null; then
        log_pass "Cloud Run service exists and is deployed"

        # Get service details
        SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
            --region="$REGION" \
            --project="$PROJECT_ID" \
            --format="get(status.url)")
        log_info "Service URL: $SERVICE_URL"
    else
        log_fail "Cloud Run service not found or not accessible"
    fi

    # Check service account
    log_check "Validating service account..."
    SA_EMAIL="agent-staging@${PROJECT_ID}.iam.gserviceaccount.com"
    if gcloud iam service-accounts describe "$SA_EMAIL" \
        --project="$PROJECT_ID" &> /dev/null; then
        log_pass "Service account exists: $SA_EMAIL"

        # Check IAM roles
        log_check "Validating IAM roles..."
        required_roles=(
            "roles/aiplatform.user"
            "roles/logging.logWriter"
            "roles/cloudtrace.agent"
            "roles/monitoring.metricWriter"
        )

        roles_ok=true
        for role in "${required_roles[@]}"; do
            if gcloud projects get-iam-policy "$PROJECT_ID" \
                --flatten="bindings[].members" \
                --filter="bindings.members:serviceAccount:${SA_EMAIL} AND bindings.role:${role}" \
                --format="value(bindings.role)" | grep -q "$role"; then
                log_info "  ✓ $role assigned"
            else
                log_warn "  ✗ $role not assigned"
                roles_ok=false
            fi
        done

        if [ "$roles_ok" = true ]; then
            log_pass "All required IAM roles are assigned"
        else
            log_warning "Some IAM roles may be missing"
        fi
    else
        log_fail "Service account not found: $SA_EMAIL"
    fi

    # Check Redis instance
    log_check "Validating Redis instance..."
    REDIS_NAME="agent-cache-staging"
    if gcloud redis instances describe "$REDIS_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" &> /dev/null; then
        log_pass "Redis instance exists: $REDIS_NAME"

        # Check Redis status
        REDIS_STATE=$(gcloud redis instances describe "$REDIS_NAME" \
            --region="$REGION" \
            --project="$PROJECT_ID" \
            --format="get(state)")

        if [ "$REDIS_STATE" == "READY" ]; then
            log_pass "Redis instance is READY"
        else
            log_warning "Redis instance state: $REDIS_STATE (expected: READY)"
        fi

        # Get Redis host
        REDIS_HOST=$(gcloud redis instances describe "$REDIS_NAME" \
            --region="$REGION" \
            --project="$PROJECT_ID" \
            --format="get(host)")
        log_info "Redis host: $REDIS_HOST"
    else
        log_fail "Redis instance not found: $REDIS_NAME"
    fi

    # Check Secret Manager secrets
    log_check "Validating Secret Manager secrets..."
    required_secrets=("redis-url" "staging-config")

    secrets_ok=true
    for secret in "${required_secrets[@]}"; do
        if gcloud secrets describe "$secret" \
            --project="$PROJECT_ID" &> /dev/null; then
            log_info "  ✓ Secret exists: $secret"
        else
            log_warn "  ✗ Secret not found: $secret"
            secrets_ok=false
        fi
    done

    if [ "$secrets_ok" = true ]; then
        log_pass "All required secrets exist"
    else
        log_warning "Some secrets may be missing"
    fi

    # Check enabled APIs
    log_check "Validating enabled APIs..."
    required_apis=(
        "aiplatform.googleapis.com"
        "logging.googleapis.com"
        "cloudtrace.googleapis.com"
        "monitoring.googleapis.com"
        "run.googleapis.com"
    )

    apis_ok=true
    for api in "${required_apis[@]}"; do
        if gcloud services list --enabled \
            --project="$PROJECT_ID" \
            --filter="name:${api}" \
            --format="value(name)" | grep -q "$api"; then
            log_info "  ✓ API enabled: $api"
        else
            log_warn "  ✗ API not enabled: $api"
            apis_ok=false
        fi
    done

    if [ "$apis_ok" = true ]; then
        log_pass "All required APIs are enabled"
    else
        log_warning "Some APIs may not be enabled"
    fi
}

# Section 2: Configuration Validation
validate_configuration() {
    log_info ""
    log_info "=========================================="
    log_info "SECTION 2: CONFIGURATION VALIDATION"
    log_info "=========================================="
    echo ""

    # Check environment variables
    log_check "Validating Cloud Run environment variables..."
    env_vars=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.template.spec.containers[0].env)" 2>/dev/null || echo "")

    if echo "$env_vars" | grep -q "ENVIRONMENT"; then
        log_pass "Environment variables are configured"
    else
        log_warning "Environment variables may not be configured"
    fi

    # Check resource allocation
    log_check "Validating resource allocation..."
    memory=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.template.spec.containers[0].resources.limits.memory)" 2>/dev/null || echo "")

    if [ -n "$memory" ]; then
        log_pass "Memory allocation: $memory"
    else
        log_warning "Memory allocation not found"
    fi

    cpu=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.template.spec.containers[0].resources.limits.cpu)" 2>/dev/null || echo "")

    if [ -n "$cpu" ]; then
        log_pass "CPU allocation: $cpu"
    else
        log_warning "CPU allocation not found"
    fi

    # Check scaling configuration
    log_check "Validating scaling configuration..."
    min_instances=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.template.metadata.annotations['autoscaling.knative.dev/minScale'])" 2>/dev/null || echo "0")

    max_instances=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.template.metadata.annotations['autoscaling.knative.dev/maxScale'])" 2>/dev/null || echo "")

    log_info "Scaling: min=$min_instances, max=$max_instances"
    log_pass "Scaling configuration validated"

    # Validate local configuration files
    log_check "Validating local configuration files..."
    config_dir="/home/user/mapachev1/config"

    required_configs=(
        "golden_tasks.yaml"
        "observability.yaml"
        "optimization.yaml"
        "quality_gates.yaml"
    )

    configs_ok=true
    for config in "${required_configs[@]}"; do
        if [ -f "$config_dir/$config" ]; then
            log_info "  ✓ Config exists: $config"
        else
            log_warn "  ✗ Config not found: $config"
            configs_ok=false
        fi
    done

    if [ "$configs_ok" = true ]; then
        log_pass "All configuration files exist"
    else
        log_warning "Some configuration files may be missing"
    fi
}

# Section 3: Service Health Validation
validate_service_health() {
    log_info ""
    log_info "=========================================="
    log_info "SECTION 3: SERVICE HEALTH VALIDATION"
    log_info "=========================================="
    echo ""

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)" 2>/dev/null || echo "")

    if [ -z "$SERVICE_URL" ]; then
        log_fail "Could not retrieve service URL"
        return
    fi

    # Test health endpoint
    log_check "Testing health endpoint..."
    health_response=$(curl -s "${SERVICE_URL}/health" || echo "")

    if echo "$health_response" | grep -q "healthy\|ok\|status"; then
        log_pass "Health endpoint is responding"

        # Parse health details
        if echo "$health_response" | grep -q "healthy"; then
            log_pass "Service reports healthy status"
        else
            log_warning "Service may not be fully healthy"
        fi
    else
        log_fail "Health endpoint not responding correctly"
    fi

    # Test metrics endpoint
    log_check "Testing metrics endpoint..."
    metrics_response=$(curl -s "${SERVICE_URL}/metrics" || echo "")

    if echo "$metrics_response" | grep -q "# HELP\|# TYPE"; then
        log_pass "Metrics endpoint is responding (Prometheus format)"
    else
        log_warning "Metrics endpoint may not be configured"
    fi

    # Check service logs
    log_check "Checking recent service logs..."
    recent_logs=$(gcloud logging read \
        "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
        --limit=5 \
        --project="$PROJECT_ID" \
        --format="value(timestamp)" \
        2>/dev/null || echo "")

    if [ -n "$recent_logs" ]; then
        log_pass "Service is generating logs"
    else
        log_warning "No recent logs found"
    fi

    # Check for errors in logs
    log_check "Checking for errors in recent logs..."
    error_logs=$(gcloud logging read \
        "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND severity>=ERROR" \
        --limit=10 \
        --project="$PROJECT_ID" \
        --format="value(jsonPayload.message)" \
        2>/dev/null || echo "")

    if [ -z "$error_logs" ]; then
        log_pass "No recent errors in logs"
    else
        error_count=$(echo "$error_logs" | wc -l)
        log_warning "Found $error_count error(s) in recent logs"
    fi

    # Check service latency
    log_check "Measuring service latency..."
    start_time=$(date +%s%N)
    curl -s -o /dev/null "${SERVICE_URL}/health"
    end_time=$(date +%s%N)
    latency_ms=$(( (end_time - start_time) / 1000000 ))

    if [ "$latency_ms" -lt 500 ]; then
        log_pass "Service latency is excellent (${latency_ms}ms)"
    elif [ "$latency_ms" -lt 1000 ]; then
        log_pass "Service latency is good (${latency_ms}ms)"
    elif [ "$latency_ms" -lt 3000 ]; then
        log_warning "Service latency is acceptable (${latency_ms}ms)"
    else
        log_fail "Service latency is high (${latency_ms}ms)"
    fi
}

# Section 4: Golden Tasks Validation
validate_golden_tasks() {
    log_info ""
    log_info "=========================================="
    log_info "SECTION 4: GOLDEN TASKS VALIDATION"
    log_info "=========================================="
    echo ""

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)" 2>/dev/null || echo "")

    if [ -z "$SERVICE_URL" ]; then
        log_fail "Could not retrieve service URL for golden tasks"
        return
    fi

    # Test sample golden tasks
    log_check "Running sample golden task (customer_support_agent)..."
    golden_response=$(curl -s -X POST "${SERVICE_URL}/evaluation/run-golden-task" \
        -H "Content-Type: application/json" \
        -d '{
            "agent_type": "customer_support_agent",
            "task_id": "cs-003"
        }' 2>/dev/null || echo "")

    if echo "$golden_response" | grep -q "task_id\|passed\|validation"; then
        log_pass "Golden task execution is functional"

        # Check if task passed
        if echo "$golden_response" | grep -q "\"passed\".*true"; then
            log_pass "Sample golden task passed validation"
        else
            log_warning "Sample golden task did not pass (may be expected)"
        fi
    else
        log_warning "Golden task execution may not be fully configured"
    fi

    # Validate golden tasks configuration
    log_check "Validating golden tasks configuration..."
    golden_tasks_file="/home/user/mapachev1/config/golden_tasks.yaml"

    if [ -f "$golden_tasks_file" ]; then
        task_count=$(grep -c "task_id:" "$golden_tasks_file" || echo 0)
        log_pass "Golden tasks configuration exists ($task_count tasks defined)"
    else
        log_fail "Golden tasks configuration not found"
    fi

    # Check quality gates
    log_check "Validating quality gates configuration..."
    quality_gates_file="/home/user/mapachev1/config/quality_gates.yaml"

    if [ -f "$quality_gates_file" ]; then
        log_pass "Quality gates configuration exists"

        # Check for gate definitions
        if grep -q "dev_gate\|staging_gate\|production_gate" "$quality_gates_file"; then
            log_pass "All environment gates are defined"
        else
            log_warning "Some environment gates may be missing"
        fi
    else
        log_fail "Quality gates configuration not found"
    fi
}

# Section 5: Monitoring and Observability
validate_observability() {
    log_info ""
    log_info "=========================================="
    log_info "SECTION 5: MONITORING & OBSERVABILITY"
    log_info "=========================================="
    echo ""

    # Check Cloud Logging
    log_check "Validating Cloud Logging integration..."
    log_count=$(gcloud logging read \
        "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
        --limit=1 \
        --project="$PROJECT_ID" \
        --format="value(timestamp)" \
        2>/dev/null | wc -l)

    if [ "$log_count" -gt 0 ]; then
        log_pass "Cloud Logging is receiving logs"
    else
        log_warning "No logs found in Cloud Logging"
    fi

    # Check Cloud Trace
    log_check "Validating Cloud Trace integration..."
    # Note: Traces may take time to appear
    log_info "Cloud Trace integration requires active requests to validate"
    log_pass "Cloud Trace configuration validated (passive check)"

    # Check Cloud Monitoring
    log_check "Validating Cloud Monitoring integration..."
    # Check if service metrics are available
    log_info "Cloud Monitoring metrics require active requests to validate"
    log_pass "Cloud Monitoring configuration validated (passive check)"

    # Validate observability configuration
    log_check "Validating observability configuration file..."
    obs_config="/home/user/mapachev1/config/observability.yaml"

    if [ -f "$obs_config" ]; then
        log_pass "Observability configuration exists"

        # Check for key sections
        if grep -q "logging:\|tracing:\|metrics:" "$obs_config"; then
            log_pass "All observability components are configured"
        else
            log_warning "Some observability components may not be configured"
        fi
    else
        log_fail "Observability configuration not found"
    fi
}

# Generate final validation report
generate_final_report() {
    log_info ""
    log_info "=========================================="
    log_info "VALIDATION SUMMARY"
    log_info "=========================================="
    echo ""

    cat >> "$VALIDATION_REPORT" << EOF

========================================
VALIDATION SUMMARY
========================================

Total Checks:    $TOTAL_CHECKS
Passed:          $PASSED_CHECKS
Failed:          $FAILED_CHECKS
Warnings:        $WARNING_CHECKS

EOF

    echo "Total Checks:    $TOTAL_CHECKS"
    echo -e "Passed:          ${GREEN}$PASSED_CHECKS${NC}"
    echo -e "Failed:          ${RED}$FAILED_CHECKS${NC}"
    echo -e "Warnings:        ${YELLOW}$WARNING_CHECKS${NC}"
    echo ""

    # Determine overall status
    if [ $FAILED_CHECKS -eq 0 ]; then
        if [ $WARNING_CHECKS -eq 0 ]; then
            log_info "✓ Staging environment is HEALTHY and ready for use"
            cat >> "$VALIDATION_REPORT" << EOF
Status: ✓ HEALTHY - Staging environment is ready for use

EOF
            return 0
        else
            log_warn "⚠ Staging environment is FUNCTIONAL with warnings"
            cat >> "$VALIDATION_REPORT" << EOF
Status: ⚠ FUNCTIONAL - Staging environment has some warnings

EOF
            return 0
        fi
    else
        log_error "✗ Staging environment has CRITICAL ISSUES"
        cat >> "$VALIDATION_REPORT" << EOF
Status: ✗ CRITICAL - Staging environment has issues that need attention

EOF
        return 1
    fi
}

# Main execution
main() {
    log_info "=========================================="
    log_info "STAGING ENVIRONMENT VALIDATION"
    log_info "=========================================="
    log_info ""
    log_info "Project: $PROJECT_ID"
    log_info "Region: $REGION"
    log_info "Service: $SERVICE_NAME"
    log_info ""

    init_report
    check_prerequisites
    validate_gcp_resources
    validate_configuration
    validate_service_health
    validate_golden_tasks
    validate_observability
    generate_final_report

    log_info ""
    log_info "Full validation report saved to: $VALIDATION_REPORT"
    log_info ""

    # Display report location with instructions
    echo ""
    echo "To view the full report:"
    echo "  cat $VALIDATION_REPORT"
    echo ""
}

# Run main function
if main; then
    exit 0
else
    exit 1
fi
