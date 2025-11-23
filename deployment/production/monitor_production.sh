#!/bin/bash
# Production Continuous Monitoring Script
# Monitors SLOs and alerts on violations

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
LOG_FILE="/tmp/monitor-production-$(date +%Y%m%d-%H%M%S).log"
HEALTH_REPORT_INTERVAL=300  # 5 minutes in seconds

# SLO Thresholds
SLO_SUCCESS_RATE=0.99        # Must be > 99%
SLO_ERROR_RATE=0.01          # Must be < 1%
SLO_P95_LATENCY=5000         # Must be < 5000ms
SLO_COST_DEVIATION=0.20      # Must be < 20%
SLO_AVAILABILITY=0.999       # Must be > 99.9%

# Alert thresholds (for warnings)
WARN_SUCCESS_RATE=0.995      # Warn if < 99.5%
WARN_ERROR_RATE=0.005        # Warn if > 0.5%
WARN_P95_LATENCY=4000        # Warn if > 4000ms
WARN_COST_DEVIATION=0.15     # Warn if > 15%

# Tracking
VIOLATIONS_COUNT=0
WARNINGS_COUNT=0
BASELINE_COST=0

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

log_slo() {
    echo -e "${CYAN}[SLO]${NC} $1" | tee -a "$LOG_FILE"
}

log_metric() {
    echo -e "${MAGENTA}[METRIC]${NC} $1" | tee -a "$LOG_FILE"
}

log_alert() {
    echo -e "${RED}[ALERT]${NC} $1" | tee -a "$LOG_FILE"
}

# Check prerequisites
check_prerequisites() {
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
}

# Get current metrics
get_current_metrics() {
    local time_window="${1:-5m}"  # Default 5 minute window

    # Get total request count
    METRIC_TOTAL_REQUESTS=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_count" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    # Get error count (5xx responses)
    METRIC_ERROR_COUNT=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_count AND metric.labels.response_code_class=5xx" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    # Calculate rates
    if [ "$METRIC_TOTAL_REQUESTS" != "0" ] && [ -n "$METRIC_TOTAL_REQUESTS" ]; then
        METRIC_ERROR_RATE=$(echo "scale=6; $METRIC_ERROR_COUNT / $METRIC_TOTAL_REQUESTS" | bc)
        METRIC_SUCCESS_RATE=$(echo "scale=6; 1 - $METRIC_ERROR_RATE" | bc)
    else
        METRIC_ERROR_RATE="0"
        METRIC_SUCCESS_RATE="1"
    fi

    # Get P95 latency
    METRIC_P95_LATENCY=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[95])" \
        --limit=1 2>/dev/null || echo "0")

    # Get P50 latency
    METRIC_P50_LATENCY=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[50])" \
        --limit=1 2>/dev/null || echo "0")

    # Get P99 latency
    METRIC_P99_LATENCY=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/request_latencies" \
        --project="$PROJECT_ID" \
        --format="value(point.value.distributionValue.percentiles[99])" \
        --limit=1 2>/dev/null || echo "0")

    # Get instance count
    METRIC_INSTANCE_COUNT=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/container/instance_count" \
        --project="$PROJECT_ID" \
        --format="value(point.value.int64Value)" \
        --limit=1 2>/dev/null || echo "0")

    # Get CPU utilization
    METRIC_CPU_UTILIZATION=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/container/cpu/utilizations" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    # Convert CPU to percentage
    METRIC_CPU_PERCENT=$(echo "scale=2; $METRIC_CPU_UTILIZATION * 100" | bc)

    # Get memory utilization
    METRIC_MEMORY_UTILIZATION=$(gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND metric.type=run.googleapis.com/container/memory/utilizations" \
        --project="$PROJECT_ID" \
        --format="value(point.value.doubleValue)" \
        --limit=1 2>/dev/null || echo "0")

    # Convert memory to percentage
    METRIC_MEMORY_PERCENT=$(echo "scale=2; $METRIC_MEMORY_UTILIZATION * 100" | bc)
}

# Get cost metrics
get_cost_metrics() {
    log_step "Fetching cost metrics..."

    # Get current month cost
    local current_month=$(date +%Y-%m)
    METRIC_CURRENT_COST=$(gcloud billing accounts list \
        --format="value(name)" 2>/dev/null | head -n1 || echo "0")

    # For demonstration, we'll use a placeholder
    # In production, you'd integrate with Cloud Billing API
    METRIC_CURRENT_COST="100.00"  # Placeholder

    # Set baseline on first run
    if [ "$BASELINE_COST" = "0" ]; then
        BASELINE_COST="$METRIC_CURRENT_COST"
    fi

    # Calculate deviation
    if [ "$BASELINE_COST" != "0" ]; then
        METRIC_COST_DEVIATION=$(echo "scale=4; ($METRIC_CURRENT_COST - $BASELINE_COST) / $BASELINE_COST" | bc)
        METRIC_COST_DEVIATION=${METRIC_COST_DEVIATION#-}  # Absolute value
    else
        METRIC_COST_DEVIATION="0"
    fi
}

# Check SLO: Success Rate
check_slo_success_rate() {
    log_slo "Checking Success Rate SLO..."

    if (( $(echo "$METRIC_SUCCESS_RATE < $SLO_SUCCESS_RATE" | bc -l) )); then
        log_alert "✗ SLO VIOLATION: Success rate $METRIC_SUCCESS_RATE < $SLO_SUCCESS_RATE"
        VIOLATIONS_COUNT=$((VIOLATIONS_COUNT + 1))
        send_slo_alert "SUCCESS_RATE" "$METRIC_SUCCESS_RATE" "$SLO_SUCCESS_RATE"
        return 1
    elif (( $(echo "$METRIC_SUCCESS_RATE < $WARN_SUCCESS_RATE" | bc -l) )); then
        log_warn "⚠ WARNING: Success rate $METRIC_SUCCESS_RATE < $WARN_SUCCESS_RATE"
        WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        return 0
    else
        log_info "✓ Success rate: $METRIC_SUCCESS_RATE (SLO: >$SLO_SUCCESS_RATE)"
        return 0
    fi
}

# Check SLO: Error Rate
check_slo_error_rate() {
    log_slo "Checking Error Rate SLO..."

    if (( $(echo "$METRIC_ERROR_RATE > $SLO_ERROR_RATE" | bc -l) )); then
        log_alert "✗ SLO VIOLATION: Error rate $METRIC_ERROR_RATE > $SLO_ERROR_RATE"
        VIOLATIONS_COUNT=$((VIOLATIONS_COUNT + 1))
        send_slo_alert "ERROR_RATE" "$METRIC_ERROR_RATE" "$SLO_ERROR_RATE"
        return 1
    elif (( $(echo "$METRIC_ERROR_RATE > $WARN_ERROR_RATE" | bc -l) )); then
        log_warn "⚠ WARNING: Error rate $METRIC_ERROR_RATE > $WARN_ERROR_RATE"
        WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        return 0
    else
        log_info "✓ Error rate: $METRIC_ERROR_RATE (SLO: <$SLO_ERROR_RATE)"
        return 0
    fi
}

# Check SLO: P95 Latency
check_slo_p95_latency() {
    log_slo "Checking P95 Latency SLO..."

    if (( $(echo "$METRIC_P95_LATENCY > $SLO_P95_LATENCY" | bc -l) )); then
        log_alert "✗ SLO VIOLATION: P95 latency ${METRIC_P95_LATENCY}ms > ${SLO_P95_LATENCY}ms"
        VIOLATIONS_COUNT=$((VIOLATIONS_COUNT + 1))
        send_slo_alert "P95_LATENCY" "$METRIC_P95_LATENCY" "$SLO_P95_LATENCY"
        return 1
    elif (( $(echo "$METRIC_P95_LATENCY > $WARN_P95_LATENCY" | bc -l) )); then
        log_warn "⚠ WARNING: P95 latency ${METRIC_P95_LATENCY}ms > ${WARN_P95_LATENCY}ms"
        WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        return 0
    else
        log_info "✓ P95 latency: ${METRIC_P95_LATENCY}ms (SLO: <${SLO_P95_LATENCY}ms)"
        return 0
    fi
}

# Check SLO: Cost Deviation
check_slo_cost_deviation() {
    log_slo "Checking Cost Deviation SLO..."

    if (( $(echo "$METRIC_COST_DEVIATION > $SLO_COST_DEVIATION" | bc -l) )); then
        log_alert "✗ SLO VIOLATION: Cost deviation $(echo "scale=0; $METRIC_COST_DEVIATION * 100" | bc)% > $(echo "scale=0; $SLO_COST_DEVIATION * 100" | bc)%"
        VIOLATIONS_COUNT=$((VIOLATIONS_COUNT + 1))
        send_slo_alert "COST_DEVIATION" "$METRIC_COST_DEVIATION" "$SLO_COST_DEVIATION"
        return 1
    elif (( $(echo "$METRIC_COST_DEVIATION > $WARN_COST_DEVIATION" | bc -l) )); then
        log_warn "⚠ WARNING: Cost deviation $(echo "scale=0; $METRIC_COST_DEVIATION * 100" | bc)% > $(echo "scale=0; $WARN_COST_DEVIATION * 100" | bc)%"
        WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        return 0
    else
        log_info "✓ Cost deviation: $(echo "scale=0; $METRIC_COST_DEVIATION * 100" | bc)% (SLO: <$(echo "scale=0; $SLO_COST_DEVIATION * 100" | bc)%)"
        return 0
    fi
}

# Send SLO violation alert
send_slo_alert() {
    local slo_type="$1"
    local current_value="$2"
    local threshold="$3"

    local alert_message="🚨 SLO VIOLATION: ${slo_type}
Service: $SERVICE_NAME
Current: $current_value
Threshold: $threshold
Project: $PROJECT_ID
Time: $(date)"

    # Log to Cloud Logging
    gcloud logging write slo-violation \
        "{\"slo\": \"$slo_type\", \"current\": \"$current_value\", \"threshold\": \"$threshold\", \"service\": \"$SERVICE_NAME\"}" \
        --severity=ERROR \
        --project="$PROJECT_ID" 2>/dev/null || true

    # Send to Slack if configured
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"$alert_message\"}" 2>/dev/null || true
    fi

    # Log alert
    log_alert "$alert_message"
}

# Display current metrics
display_current_metrics() {
    echo ""
    echo "=========================================="
    echo "  CURRENT PRODUCTION METRICS"
    echo "=========================================="
    echo ""

    log_metric "TRAFFIC:"
    log_metric "  Total Requests:    $METRIC_TOTAL_REQUESTS"
    log_metric "  Error Count:       $METRIC_ERROR_COUNT"
    echo ""

    log_metric "SUCCESS & ERRORS:"
    log_metric "  Success Rate:      $METRIC_SUCCESS_RATE (SLO: >$SLO_SUCCESS_RATE)"
    log_metric "  Error Rate:        $METRIC_ERROR_RATE (SLO: <$SLO_ERROR_RATE)"
    echo ""

    log_metric "LATENCY:"
    log_metric "  P50 Latency:       ${METRIC_P50_LATENCY}ms"
    log_metric "  P95 Latency:       ${METRIC_P95_LATENCY}ms (SLO: <${SLO_P95_LATENCY}ms)"
    log_metric "  P99 Latency:       ${METRIC_P99_LATENCY}ms"
    echo ""

    log_metric "RESOURCES:"
    log_metric "  Instance Count:    $METRIC_INSTANCE_COUNT"
    log_metric "  CPU Utilization:   ${METRIC_CPU_PERCENT}%"
    log_metric "  Memory Util:       ${METRIC_MEMORY_PERCENT}%"
    echo ""

    log_metric "COSTS:"
    log_metric "  Current Cost:      \$${METRIC_CURRENT_COST}"
    log_metric "  Baseline Cost:     \$${BASELINE_COST}"
    log_metric "  Cost Deviation:    $(echo "scale=0; $METRIC_COST_DEVIATION * 100" | bc)% (SLO: <$(echo "scale=0; $SLO_COST_DEVIATION * 100" | bc)%)"
    echo ""
}

# Run all SLO checks
run_slo_checks() {
    log_step "Running SLO checks..."

    VIOLATIONS_COUNT=0
    WARNINGS_COUNT=0

    check_slo_success_rate
    check_slo_error_rate
    check_slo_p95_latency
    check_slo_cost_deviation

    echo ""
    if [ $VIOLATIONS_COUNT -gt 0 ]; then
        log_alert "SLO Check Result: $VIOLATIONS_COUNT VIOLATIONS, $WARNINGS_COUNT warnings"
        return 1
    elif [ $WARNINGS_COUNT -gt 0 ]; then
        log_warn "SLO Check Result: $WARNINGS_COUNT warnings"
        return 0
    else
        log_info "SLO Check Result: All SLOs met ✓"
        return 0
    fi
}

# Generate health report
generate_health_report() {
    local report_file="/tmp/health-report-$(date +%Y%m%d-%H%M%S).txt"

    cat > "$report_file" << EOF
===============================================
PRODUCTION HEALTH REPORT
===============================================

Generated: $(date)
Service: $SERVICE_NAME
Project: $PROJECT_ID
Region: $REGION

TRAFFIC METRICS:
----------------
Total Requests:    $METRIC_TOTAL_REQUESTS
Error Count:       $METRIC_ERROR_COUNT

SUCCESS & ERROR RATES:
----------------------
Success Rate:      $METRIC_SUCCESS_RATE
  SLO:            >$SLO_SUCCESS_RATE
  Status:         $(if (( $(echo "$METRIC_SUCCESS_RATE >= $SLO_SUCCESS_RATE" | bc -l) )); then echo "PASS"; else echo "FAIL"; fi)

Error Rate:        $METRIC_ERROR_RATE
  SLO:            <$SLO_ERROR_RATE
  Status:         $(if (( $(echo "$METRIC_ERROR_RATE <= $SLO_ERROR_RATE" | bc -l) )); then echo "PASS"; else echo "FAIL"; fi)

LATENCY METRICS:
----------------
P50 Latency:       ${METRIC_P50_LATENCY}ms
P95 Latency:       ${METRIC_P95_LATENCY}ms
  SLO:            <${SLO_P95_LATENCY}ms
  Status:         $(if (( $(echo "$METRIC_P95_LATENCY <= $SLO_P95_LATENCY" | bc -l) )); then echo "PASS"; else echo "FAIL"; fi)
P99 Latency:       ${METRIC_P99_LATENCY}ms

RESOURCE UTILIZATION:
---------------------
Instance Count:    $METRIC_INSTANCE_COUNT
CPU Utilization:   ${METRIC_CPU_PERCENT}%
Memory Util:       ${METRIC_MEMORY_PERCENT}%

COST METRICS:
-------------
Current Cost:      \$${METRIC_CURRENT_COST}
Baseline Cost:     \$${BASELINE_COST}
Cost Deviation:    $(echo "scale=0; $METRIC_COST_DEVIATION * 100" | bc)%
  SLO:            <$(echo "scale=0; $SLO_COST_DEVIATION * 100" | bc)%
  Status:         $(if (( $(echo "$METRIC_COST_DEVIATION <= $SLO_COST_DEVIATION" | bc -l) )); then echo "PASS"; else echo "FAIL"; fi)

OVERALL STATUS:
---------------
SLO Violations:    $VIOLATIONS_COUNT
Warnings:          $WARNINGS_COUNT
Health Status:     $(if [ $VIOLATIONS_COUNT -eq 0 ]; then echo "HEALTHY"; else echo "DEGRADED"; fi)

RECOMMENDATIONS:
----------------
$(if [ $VIOLATIONS_COUNT -gt 0 ]; then
    echo "- IMMEDIATE ACTION REQUIRED: SLO violations detected"
    echo "- Review error logs and recent deployments"
    echo "- Consider rollback if issues persist"
elif [ $WARNINGS_COUNT -gt 0 ]; then
    echo "- Monitor closely: Warning thresholds exceeded"
    echo "- Investigate potential issues"
else
    echo "- System operating normally"
    echo "- Continue regular monitoring"
fi)

===============================================
EOF

    log_info "Health report generated: $report_file"

    # Display report
    cat "$report_file"
    echo ""
}

# Continuous monitoring loop
continuous_monitoring() {
    log_info "Starting continuous monitoring..."
    log_info "Health reports every ${HEALTH_REPORT_INTERVAL}s ($(($HEALTH_REPORT_INTERVAL / 60)) minutes)"
    log_info "Press Ctrl+C to stop"
    echo ""

    local iteration=1

    while true; do
        log_step "Monitoring iteration #$iteration - $(date)"

        # Get metrics
        get_current_metrics
        get_cost_metrics

        # Display metrics
        display_current_metrics

        # Run SLO checks
        run_slo_checks

        # Generate health report
        if [ $((iteration % 1)) -eq 0 ]; then  # Every iteration for now
            generate_health_report
        fi

        # Wait for next check
        log_info "Next check in ${HEALTH_REPORT_INTERVAL}s..."
        log_info "=================================="
        echo ""

        sleep "$HEALTH_REPORT_INTERVAL"
        iteration=$((iteration + 1))
    done
}

# One-time monitoring check
single_check() {
    log_info "Running single monitoring check..."
    echo ""

    get_current_metrics
    get_cost_metrics
    display_current_metrics
    run_slo_checks
    generate_health_report

    if [ $VIOLATIONS_COUNT -gt 0 ]; then
        exit 1
    else
        exit 0
    fi
}

# Print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --continuous    Run continuous monitoring (default)"
    echo "  --once          Run a single check and exit"
    echo "  --help          Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  GCP_PROJECT_ID      GCP project ID (required)"
    echo "  GCP_REGION          GCP region (default: us-central1)"
    echo "  SLACK_WEBHOOK_URL   Slack webhook for alerts (optional)"
    echo ""
    echo "SLO Thresholds:"
    echo "  Success Rate:   >$SLO_SUCCESS_RATE (>99%)"
    echo "  Error Rate:     <$SLO_ERROR_RATE (<1%)"
    echo "  P95 Latency:    <${SLO_P95_LATENCY}ms"
    echo "  Cost Deviation: <$(echo "scale=0; $SLO_COST_DEVIATION * 100" | bc)% (<20%)"
    echo ""
}

# Main execution
main() {
    local mode="continuous"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --continuous)
                mode="continuous"
                shift
                ;;
            --once)
                mode="once"
                shift
                ;;
            --help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done

    log_info "=========================================="
    log_info "  PRODUCTION MONITORING"
    log_info "=========================================="
    log_info ""
    log_info "Service: $SERVICE_NAME"
    log_info "Project: $PROJECT_ID"
    log_info "Mode: $mode"
    log_info "Log file: $LOG_FILE"
    log_info ""

    check_prerequisites

    if [ "$mode" = "continuous" ]; then
        continuous_monitoring
    else
        single_check
    fi
}

# Run main function
main "$@"
