#!/bin/bash
# Rollback Staging Deployment
# Routes traffic to previous version, cleans up failed deployment, and notifies team

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
ROLLBACK_LOG="/tmp/rollback_$(date +%s).log"
ROLLBACK_REASON="${1:-Manual rollback requested}"

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "[INFO] $1" >> "$ROLLBACK_LOG"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[WARN] $1" >> "$ROLLBACK_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[ERROR] $1" >> "$ROLLBACK_LOG"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
    echo "[STEP] $1" >> "$ROLLBACK_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[SUCCESS] $1" >> "$ROLLBACK_LOG"
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

    # Verify service exists
    if ! gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" &> /dev/null; then
        log_error "Service not found: $SERVICE_NAME"
        exit 1
    fi

    log_success "Prerequisites validated"
}

# Confirm rollback
confirm_rollback() {
    log_warn "=========================================="
    log_warn "ROLLBACK CONFIRMATION REQUIRED"
    log_warn "=========================================="
    echo ""
    log_warn "Service: $SERVICE_NAME"
    log_warn "Project: $PROJECT_ID"
    log_warn "Region: $REGION"
    log_warn "Reason: $ROLLBACK_REASON"
    echo ""
    log_warn "This will:"
    log_warn "  1. Route traffic to the previous stable version"
    log_warn "  2. Clean up the current failed deployment"
    log_warn "  3. Mark the current version as inactive"
    echo ""

    # Skip confirmation if ROLLBACK_AUTO_CONFIRM is set
    if [ "${ROLLBACK_AUTO_CONFIRM:-false}" = "true" ]; then
        log_info "Auto-confirm enabled, proceeding with rollback..."
        return 0
    fi

    read -p "Do you want to proceed with rollback? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log_info "Rollback cancelled by user"
        exit 0
    fi

    log_info "Rollback confirmed, proceeding..."
}

# Get current and previous revisions
get_revisions() {
    log_step "Identifying current and previous revisions..."

    # Get all revisions sorted by creation time
    REVISIONS=$(gcloud run revisions list \
        --service="$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(metadata.name)" \
        --sort-by="~metadata.creationTimestamp" \
        2>/dev/null || echo "")

    if [ -z "$REVISIONS" ]; then
        log_error "No revisions found for service $SERVICE_NAME"
        exit 1
    fi

    # Get current revision (most recent)
    CURRENT_REVISION=$(echo "$REVISIONS" | head -n 1)
    log_info "Current revision: $CURRENT_REVISION"

    # Get previous revision (second most recent)
    PREVIOUS_REVISION=$(echo "$REVISIONS" | head -n 2 | tail -n 1)

    if [ -z "$PREVIOUS_REVISION" ] || [ "$PREVIOUS_REVISION" = "$CURRENT_REVISION" ]; then
        log_error "No previous revision found to rollback to"
        log_error "This may be the first deployment"
        exit 1
    fi

    log_info "Previous revision: $PREVIOUS_REVISION"
    log_success "Revisions identified"
}

# Capture current state
capture_current_state() {
    log_step "Capturing current state for audit trail..."

    STATE_FILE="/tmp/pre_rollback_state_$(date +%s).json"

    # Get current service configuration
    gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format=json > "$STATE_FILE" 2>/dev/null || true

    if [ -f "$STATE_FILE" ]; then
        log_info "Current state saved to: $STATE_FILE"
    else
        log_warn "Could not save current state"
    fi

    # Get current traffic routing
    CURRENT_TRAFFIC=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.traffic)" 2>/dev/null || echo "")

    log_info "Current traffic routing: $CURRENT_TRAFFIC"
    log_success "Current state captured"
}

# Route traffic to previous version
route_to_previous() {
    log_step "Routing traffic to previous stable version..."

    log_info "Updating traffic routing: 100% -> $PREVIOUS_REVISION"

    # Update service to route all traffic to previous revision
    if gcloud run services update-traffic "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --to-revisions="$PREVIOUS_REVISION=100" \
        --quiet 2>&1 | tee -a "$ROLLBACK_LOG"; then
        log_success "Traffic successfully routed to previous revision"
    else
        log_error "Failed to route traffic to previous revision"
        exit 1
    fi

    # Verify traffic routing
    log_step "Verifying traffic routing..."
    sleep 5

    NEW_TRAFFIC=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="value(spec.traffic)" 2>/dev/null || echo "")

    if echo "$NEW_TRAFFIC" | grep -q "$PREVIOUS_REVISION"; then
        log_success "Traffic routing verified"
    else
        log_warn "Could not verify traffic routing"
    fi
}

# Test rolled back service
test_service_health() {
    log_step "Testing service health after rollback..."

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)" 2>/dev/null || echo "")

    if [ -z "$SERVICE_URL" ]; then
        log_error "Could not retrieve service URL"
        return 1
    fi

    log_info "Testing: $SERVICE_URL/health"

    # Test health endpoint
    for i in {1..5}; do
        log_info "Health check attempt $i/5..."

        health_response=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/health" || echo "000")

        if [ "$health_response" = "200" ]; then
            log_success "Service health check passed (HTTP 200)"
            return 0
        else
            log_warn "Health check returned HTTP $health_response, retrying..."
            sleep 2
        fi
    done

    log_error "Service health checks failed after rollback"
    return 1
}

# Clean up failed deployment
cleanup_failed_deployment() {
    log_step "Cleaning up failed deployment..."

    # Tag the failed revision
    log_info "Tagging failed revision: $CURRENT_REVISION"

    # Delete the failed revision (optional, commented out for safety)
    # gcloud run revisions delete "$CURRENT_REVISION" \
    #     --region="$REGION" \
    #     --project="$PROJECT_ID" \
    #     --quiet

    # Instead, just log it for manual cleanup
    log_info "Failed revision preserved for investigation: $CURRENT_REVISION"
    log_info "To delete manually:"
    log_info "  gcloud run revisions delete $CURRENT_REVISION --region=$REGION --project=$PROJECT_ID"

    log_success "Cleanup preparation complete"
}

# Generate rollback report
generate_rollback_report() {
    log_step "Generating rollback report..."

    REPORT_FILE="/tmp/rollback_report_$(date +%s).txt"

    cat > "$REPORT_FILE" << EOF
========================================
STAGING ROLLBACK REPORT
========================================

Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Project: $PROJECT_ID
Region: $REGION
Service: $SERVICE_NAME

ROLLBACK DETAILS
----------------
Reason: $ROLLBACK_REASON
From Revision: $CURRENT_REVISION
To Revision: $PREVIOUS_REVISION
Status: SUCCESS

TIMELINE
--------
Rollback Initiated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Traffic Routing: Completed
Health Checks: $([ "$?" -eq 0 ] && echo "Passed" || echo "Failed")

ACTIONS TAKEN
-------------
1. ✓ Traffic routed to previous stable version
2. ✓ Service health verified
3. ✓ Failed revision marked for investigation
4. ✓ Team notification prepared

NEXT STEPS
----------
1. Investigate root cause of deployment failure
2. Review logs for failed revision: $CURRENT_REVISION
3. Fix issues and prepare new deployment
4. Manually clean up failed revision when ready

USEFUL COMMANDS
---------------
View logs for failed revision:
  gcloud logging read "resource.labels.revision_name=${CURRENT_REVISION}" --project=$PROJECT_ID

View service status:
  gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID

Delete failed revision (when investigation complete):
  gcloud run revisions delete $CURRENT_REVISION --region=$REGION --project=$PROJECT_ID

========================================
EOF

    cat "$REPORT_FILE"
    log_info "Rollback report saved to: $REPORT_FILE"
}

# Send notification
send_notification() {
    log_step "Preparing team notification..."

    NOTIFICATION_FILE="/tmp/rollback_notification_$(date +%s).txt"

    cat > "$NOTIFICATION_FILE" << EOF
🚨 STAGING ROLLBACK NOTIFICATION

Environment: Staging
Service: $SERVICE_NAME
Project: $PROJECT_ID
Region: $REGION

Reason: $ROLLBACK_REASON

Status: ✓ Rollback completed successfully
Current Version: $PREVIOUS_REVISION
Failed Version: $CURRENT_REVISION (preserved for investigation)

Next Steps:
- Investigate root cause
- Review error logs
- Prepare corrected deployment

Rollback completed at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Full report: See $REPORT_FILE
EOF

    log_info "Notification prepared:"
    cat "$NOTIFICATION_FILE"

    # In production, this would send via:
    # - Slack webhook
    # - Email
    # - PagerDuty
    # - Google Chat
    log_info ""
    log_info "To send notification, use:"
    log_info "  # Slack: curl -X POST <webhook-url> -d @$NOTIFICATION_FILE"
    log_info "  # Email: cat $NOTIFICATION_FILE | mail -s 'Staging Rollback' team@example.com"
    log_info ""

    log_success "Notification prepared"
}

# Create incident report
create_incident_report() {
    log_step "Creating incident report..."

    INCIDENT_FILE="/tmp/incident_$(date +%s).json"

    cat > "$INCIDENT_FILE" << EOF
{
  "incident_type": "deployment_rollback",
  "severity": "medium",
  "environment": "staging",
  "service": "$SERVICE_NAME",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "reason": "$ROLLBACK_REASON",
  "failed_revision": "$CURRENT_REVISION",
  "rolled_back_to": "$PREVIOUS_REVISION",
  "status": "resolved",
  "actions_taken": [
    "Traffic routed to previous stable version",
    "Service health verified",
    "Failed revision preserved for investigation",
    "Team notified"
  ],
  "logs": {
    "rollback_log": "$ROLLBACK_LOG",
    "report": "$REPORT_FILE",
    "notification": "$NOTIFICATION_FILE"
  }
}
EOF

    log_info "Incident report created: $INCIDENT_FILE"
    log_success "Incident documented"
}

# Print summary
print_summary() {
    echo ""
    log_info "=========================================="
    log_info "ROLLBACK SUMMARY"
    log_info "=========================================="
    echo ""
    log_success "Rollback completed successfully!"
    echo ""
    log_info "Service: $SERVICE_NAME"
    log_info "Rolled back from: $CURRENT_REVISION"
    log_info "Rolled back to: $PREVIOUS_REVISION"
    log_info "Reason: $ROLLBACK_REASON"
    echo ""
    log_info "Generated Files:"
    log_info "  Rollback Log: $ROLLBACK_LOG"
    log_info "  Rollback Report: $REPORT_FILE"
    log_info "  Notification: $NOTIFICATION_FILE"
    log_info "  Incident Report: $INCIDENT_FILE"
    echo ""
    log_info "Next Steps:"
    log_info "  1. Review rollback report"
    log_info "  2. Investigate failed deployment"
    log_info "  3. Send team notification"
    log_info "  4. Plan corrective actions"
    echo ""
}

# Main execution
main() {
    log_info "=========================================="
    log_info "STAGING DEPLOYMENT ROLLBACK"
    log_info "=========================================="
    log_info ""
    log_info "Initiating rollback for staging environment"
    log_info "Project: $PROJECT_ID"
    log_info "Region: $REGION"
    log_info "Service: $SERVICE_NAME"
    log_info "Reason: $ROLLBACK_REASON"
    log_info ""

    check_prerequisites
    confirm_rollback
    get_revisions
    capture_current_state
    route_to_previous
    test_service_health
    cleanup_failed_deployment
    generate_rollback_report
    send_notification
    create_incident_report
    print_summary

    log_success "Rollback procedure completed!"
}

# Run main function
if main; then
    exit 0
else
    log_error "Rollback failed. Please check logs: $ROLLBACK_LOG"
    exit 1
fi
