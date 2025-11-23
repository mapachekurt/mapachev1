#!/bin/bash
# Production Rollback Script
# Emergency rollback to last known good revision

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="agent-improvements-prod"
LOG_FILE="/tmp/rollback-$(date +%Y%m%d-%H%M%S).log"
FORENSICS_DIR="/tmp/forensics-$(date +%Y%m%d-%H%M%S)"

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

log_critical() {
    echo -e "${RED}[CRITICAL]${NC} $1" | tee -a "$LOG_FILE"
}

log_rollback() {
    echo -e "${MAGENTA}[ROLLBACK]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to require confirmation for rollback
require_confirmation() {
    echo ""
    log_critical "⚠️  PRODUCTION ROLLBACK INITIATED"
    log_critical "This will rollback production to the last stable version"
    log_critical "Project: $PROJECT_ID"
    log_critical "Service: $SERVICE_NAME"
    echo ""

    if [ "${EMERGENCY_ROLLBACK:-false}" = "true" ]; then
        log_warn "EMERGENCY_ROLLBACK flag set, skipping confirmation"
        return
    fi

    read -p "Are you ABSOLUTELY SURE you want to rollback? (type 'ROLLBACK' to confirm): " confirmation

    if [ "$confirmation" != "ROLLBACK" ]; then
        log_error "Rollback cancelled by user"
        exit 1
    fi
    log_info "Rollback confirmed, proceeding..."
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

    log_info "Prerequisites check passed ✓"
}

# Create forensics directory
create_forensics_dir() {
    log_step "Creating forensics directory..."

    mkdir -p "$FORENSICS_DIR"
    log_info "Forensics directory: $FORENSICS_DIR"
}

# Capture current state for forensics
capture_current_state() {
    log_step "Capturing current state for forensics analysis..."

    # Get current service configuration
    gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format=json > "${FORENSICS_DIR}/service-state.json" 2>/dev/null || true

    # Get current traffic split
    gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.traffic)" > "${FORENSICS_DIR}/traffic-split.txt" 2>/dev/null || true

    # Get recent logs
    log_info "Capturing recent error logs..."
    gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME} AND severity>=ERROR" \
        --limit=100 \
        --project="$PROJECT_ID" \
        --format=json > "${FORENSICS_DIR}/error-logs.json" 2>/dev/null || true

    # Get metrics snapshots
    log_info "Capturing metrics snapshot..."
    gcloud monitoring time-series list \
        --filter="resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
        --project="$PROJECT_ID" \
        --format=json > "${FORENSICS_DIR}/metrics-snapshot.json" 2>/dev/null || true

    # List all revisions
    gcloud run revisions list \
        --service="$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format=json > "${FORENSICS_DIR}/all-revisions.json" 2>/dev/null || true

    log_info "Forensics data captured ✓"
    log_info "Forensics location: $FORENSICS_DIR"
}

# Identify current and stable revisions
identify_revisions() {
    log_step "Identifying current and stable revisions..."

    # Get current traffic distribution
    CURRENT_REVISION=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.latestReadyRevisionName)")

    log_info "Current latest revision: $CURRENT_REVISION"

    # Get all revisions sorted by creation time
    mapfile -t ALL_REVISIONS < <(gcloud run revisions list \
        --service="$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(metadata.name)" \
        --sort-by="~metadata.creationTimestamp")

    log_info "Total revisions found: ${#ALL_REVISIONS[@]}"

    # Find stable revision (second most recent, or user-specified)
    if [ -n "${TARGET_REVISION:-}" ]; then
        STABLE_REVISION="$TARGET_REVISION"
        log_warn "Using user-specified target revision: $STABLE_REVISION"
    elif [ ${#ALL_REVISIONS[@]} -ge 2 ]; then
        STABLE_REVISION="${ALL_REVISIONS[1]}"
        log_info "Auto-detected stable revision: $STABLE_REVISION"
    else
        log_error "Not enough revisions to rollback. Need at least 2 revisions."
        exit 1
    fi

    # Verify stable revision exists
    if ! gcloud run revisions describe "$STABLE_REVISION" \
        --region="$REGION" \
        --project="$PROJECT_ID" &> /dev/null; then
        log_error "Target revision $STABLE_REVISION does not exist"
        exit 1
    fi

    log_rollback "Rollback plan:"
    log_rollback "  FROM: $CURRENT_REVISION (current)"
    log_rollback "  TO:   $STABLE_REVISION (stable)"
}

# Stop any ongoing deployments
stop_ongoing_deployments() {
    log_step "Checking for ongoing deployments..."

    # List recent Cloud Build jobs
    local recent_builds=$(gcloud builds list \
        --filter="status=WORKING OR status=QUEUED" \
        --limit=10 \
        --project="$PROJECT_ID" \
        --format="value(id)" 2>/dev/null || echo "")

    if [ -n "$recent_builds" ]; then
        log_warn "Found ongoing builds, cancelling..."
        while IFS= read -r build_id; do
            if [ -n "$build_id" ]; then
                log_info "Cancelling build: $build_id"
                gcloud builds cancel "$build_id" --project="$PROJECT_ID" 2>/dev/null || true
            fi
        done <<< "$recent_builds"
        log_info "All ongoing builds cancelled"
    else
        log_info "No ongoing builds found"
    fi
}

# Execute rollback
execute_rollback() {
    log_step "Executing rollback to stable revision..."

    log_rollback "Routing 100% traffic to: $STABLE_REVISION"

    # Route all traffic to stable revision
    gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="${STABLE_REVISION}=100" | tee -a "$LOG_FILE"

    log_rollback "Traffic shifted to stable revision ✓"
}

# Verify rollback success
verify_rollback() {
    log_step "Verifying rollback success..."

    # Wait a moment for traffic to shift
    sleep 10

    # Check current traffic split
    local current_traffic=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.traffic[0].revisionName,status.traffic[0].percent)")

    log_info "Current traffic: $current_traffic"

    # Verify stable revision is getting 100% traffic
    if echo "$current_traffic" | grep -q "$STABLE_REVISION.*100"; then
        log_rollback "Rollback verified - 100% traffic on stable revision ✓"
    else
        log_error "Rollback verification failed"
        log_error "Current traffic distribution: $current_traffic"
        return 1
    fi

    # Run health checks
    log_info "Running health checks on stable revision..."

    local service_url=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(status.url)")

    local health_check_passed=false
    for i in {1..5}; do
        log_info "Health check attempt $i/5..."
        if curl -s -f -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
            "${service_url}/health" | grep -q "healthy"; then
            log_rollback "Health check passed ✓"
            health_check_passed=true
            break
        fi
        sleep 5
    done

    if [ "$health_check_passed" = false ]; then
        log_error "Health checks failed on stable revision"
        return 1
    fi

    log_rollback "Rollback verification complete ✓"
}

# Clean up failed deployments
cleanup_failed_deployments() {
    log_step "Cleaning up failed deployments..."

    if [ "$CURRENT_REVISION" != "$STABLE_REVISION" ]; then
        log_info "Considering cleanup of failed revision: $CURRENT_REVISION"

        if [ "${AUTO_CLEANUP:-false}" = "true" ]; then
            log_warn "AUTO_CLEANUP enabled, deleting failed revision..."
            gcloud run revisions delete "$CURRENT_REVISION" \
                --region="$REGION" \
                --project="$PROJECT_ID" \
                --quiet 2>/dev/null || log_warn "Could not delete failed revision"
            log_info "Failed revision deleted"
        else
            log_info "Keeping failed revision for forensics"
            log_info "To delete manually: gcloud run revisions delete $CURRENT_REVISION --region=$REGION --project=$PROJECT_ID"
        fi
    fi

    # Clean up untagged/old revisions (older than 7 days)
    log_info "Cleaning up old revisions (>7 days)..."
    local old_date=$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)

    gcloud run revisions list \
        --service="$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --filter="metadata.creationTimestamp<${old_date}" \
        --format="value(metadata.name)" | while read -r old_revision; do
        if [ -n "$old_revision" ] && [ "$old_revision" != "$STABLE_REVISION" ]; then
            log_info "Deleting old revision: $old_revision"
            gcloud run revisions delete "$old_revision" \
                --region="$REGION" \
                --project="$PROJECT_ID" \
                --quiet 2>/dev/null || true
        fi
    done

    log_info "Cleanup complete ✓"
}

# Send critical alerts
send_critical_alerts() {
    log_step "Sending critical alerts..."

    local alert_message="PRODUCTION ROLLBACK EXECUTED
Service: $SERVICE_NAME
Project: $PROJECT_ID
Region: $REGION
Rolled back FROM: $CURRENT_REVISION
Rolled back TO: $STABLE_REVISION
Timestamp: $(date)
Forensics: $FORENSICS_DIR"

    # Log to Cloud Logging with CRITICAL severity
    gcloud logging write production-rollback \
        "{\"event\": \"rollback\", \"service\": \"$SERVICE_NAME\", \"from\": \"$CURRENT_REVISION\", \"to\": \"$STABLE_REVISION\"}" \
        --severity=CRITICAL \
        --project="$PROJECT_ID" 2>/dev/null || log_warn "Could not send to Cloud Logging"

    # Send to Slack if configured
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        log_info "Sending Slack notification..."
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"🚨 PRODUCTION ROLLBACK\n\`\`\`${alert_message}\`\`\`\"}" 2>/dev/null || log_warn "Could not send Slack notification"
    fi

    # Send email if configured
    if [ -n "${ALERT_EMAIL:-}" ]; then
        log_info "Alert email would be sent to: $ALERT_EMAIL"
        # Email sending would be implemented here
    fi

    log_info "Critical alerts sent ✓"
}

# Generate incident report
generate_incident_report() {
    log_step "Generating incident report..."

    local report_file="${FORENSICS_DIR}/incident-report.txt"

    cat > "$report_file" << EOF
===============================================
PRODUCTION ROLLBACK INCIDENT REPORT
===============================================

INCIDENT DETAILS:
-----------------
Timestamp: $(date)
Service: $SERVICE_NAME
Project: $PROJECT_ID
Region: $REGION
Environment: PRODUCTION

ROLLBACK DETAILS:
-----------------
Rolled back FROM: $CURRENT_REVISION
Rolled back TO:   $STABLE_REVISION
Rollback status:  SUCCESS
Health checks:    PASSED

TIMELINE:
---------
1. Rollback initiated: $(date)
2. Current state captured
3. Ongoing deployments stopped
4. Traffic shifted to stable revision
5. Rollback verified
6. Alerts sent
7. Incident report generated

FORENSICS DATA:
---------------
Location: $FORENSICS_DIR
Files:
  - service-state.json    : Service configuration at rollback time
  - traffic-split.txt     : Traffic distribution at rollback time
  - error-logs.json       : Recent error logs
  - metrics-snapshot.json : Metrics snapshot
  - all-revisions.json    : All available revisions
  - incident-report.txt   : This report

LOGS:
-----
Rollback log: $LOG_FILE

NEXT STEPS:
-----------
1. Review forensics data in: $FORENSICS_DIR
2. Analyze error logs for root cause
3. Fix issues in failed revision
4. Test fix in staging environment
5. Prepare for redeployment
6. Document learnings and update runbooks

ROLLBACK COMMAND (if needed again):
------------------------------------
./deployment/production/rollback_production.sh

REVERT ROLLBACK (deploy failed version again):
-----------------------------------------------
export TARGET_REVISION=$CURRENT_REVISION
gcloud run services update-traffic $SERVICE_NAME \\
  --region=$REGION \\
  --project=$PROJECT_ID \\
  --to-revisions=$CURRENT_REVISION=100

CONTACTS:
---------
Oncall Engineer: [Configure in production]
SRE Lead: [Configure in production]
Product Owner: [Configure in production]

===============================================
END OF INCIDENT REPORT
===============================================
EOF

    log_info "Incident report generated: $report_file"
    echo ""
    cat "$report_file"
    echo ""
}

# Create rollback summary
print_summary() {
    log_rollback ""
    log_rollback "=========================================="
    log_rollback "  ROLLBACK COMPLETE"
    log_rollback "=========================================="
    log_rollback ""
    log_rollback "Service:  $SERVICE_NAME"
    log_rollback "From:     $CURRENT_REVISION"
    log_rollback "To:       $STABLE_REVISION"
    log_rollback "Status:   SUCCESS ✓"
    log_rollback ""
    log_info "Forensics: $FORENSICS_DIR"
    log_info "Log file:  $LOG_FILE"
    log_rollback ""
    log_warn "IMPORTANT:"
    log_warn "  - Review forensics data"
    log_warn "  - Investigate root cause"
    log_warn "  - Update incident documentation"
    log_warn "  - Notify stakeholders"
    log_rollback ""
    log_info "To monitor:"
    log_info "  ./deployment/production/monitor_production.sh"
    log_rollback ""
}

# Main execution
main() {
    echo ""
    log_critical "=========================================="
    log_critical "  PRODUCTION ROLLBACK"
    log_critical "=========================================="
    echo ""
    log_critical "This script will rollback production to a stable revision"
    log_info "Log file: $LOG_FILE"
    echo ""

    require_confirmation

    check_prerequisites
    create_forensics_dir
    capture_current_state
    identify_revisions
    stop_ongoing_deployments
    execute_rollback
    verify_rollback
    cleanup_failed_deployments
    send_critical_alerts
    generate_incident_report
    print_summary

    log_rollback "Rollback procedure completed successfully ✓"
}

# Handle script arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --emergency)
            EMERGENCY_ROLLBACK=true
            shift
            ;;
        --auto-cleanup)
            AUTO_CLEANUP=true
            shift
            ;;
        --target)
            TARGET_REVISION="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --emergency        Skip confirmation prompt"
            echo "  --auto-cleanup     Automatically delete failed revision"
            echo "  --target REVISION  Specify target revision to rollback to"
            echo "  --help            Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  GCP_PROJECT_ID    GCP project ID (required)"
            echo "  GCP_REGION        GCP region (default: us-central1)"
            echo "  SLACK_WEBHOOK_URL Slack webhook for alerts (optional)"
            echo "  ALERT_EMAIL       Email for alerts (optional)"
            echo ""
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main function
main "$@"
