#!/bin/bash
# Master Deployment Orchestrator
# Single entry point for deploying Agent Production Framework
# Supports: Local Testing → Staging → Production

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Logging
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
log_success() { echo -e "${MAGENTA}[SUCCESS]${NC} $1"; }

# Banner
print_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🚀 Agent Production Framework Deployment 🚀             ║
║                                                               ║
║      7 Critical Improvements for 511+ AI Agents               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Help
show_help() {
    cat << EOF
Usage: ./deploy.sh [COMMAND] [OPTIONS]

COMMANDS:
    local       - Run local testing (Option C)
    staging     - Deploy to staging environment (Option A)
    production  - Deploy to production environment (Option B)
    all         - Run complete deployment pipeline (Local → Staging → Production)
    status      - Check deployment status across all environments
    rollback    - Rollback to previous version (requires --env flag)
    help        - Show this help message

LOCAL TESTING (Option C):
    ./deploy.sh local setup           - Set up local environment
    ./deploy.sh local integrate       - Integrate pilot agents
    ./deploy.sh local test            - Test pilot agents
    ./deploy.sh local validate        - Validate all improvements
    ./deploy.sh local metrics         - Collect metrics
    ./deploy.sh local all             - Run all local steps

STAGING (Option A):
    ./deploy.sh staging setup         - Set up staging environment
    ./deploy.sh staging deploy        - Deploy to staging
    ./deploy.sh staging test          - Run smoke tests
    ./deploy.sh staging validate      - Validate staging
    ./deploy.sh staging rollback      - Rollback staging

PRODUCTION (Option B):
    ./deploy.sh production setup      - Set up production environment
    ./deploy.sh production blue-green - Deploy with blue-green strategy
    ./deploy.sh production canary     - Deploy with canary strategy
    ./deploy.sh production monitor    - Start continuous monitoring
    ./deploy.sh production rollback   - Rollback production

COMPLETE PIPELINE:
    ./deploy.sh all                   - Local → Staging → Production
    ./deploy.sh all --skip-local      - Skip local, go directly to staging
    ./deploy.sh all --staging-only    - Stop after staging validation

OPTIONS:
    --skip-tests        Skip automated tests
    --auto-confirm      Auto-confirm all prompts
    --verbose           Verbose output
    --dry-run           Show what would be done without executing

ENVIRONMENT VARIABLES:
    GCP_PROJECT_ID      Google Cloud Project ID (required for staging/production)
    GCP_REGION          Google Cloud Region (default: us-central1)
    SLACK_WEBHOOK_URL   Slack webhook for notifications (optional)

EXAMPLES:
    # Start with local testing
    ./deploy.sh local all

    # Deploy to staging
    export GCP_PROJECT_ID=my-project
    ./deploy.sh staging setup
    ./deploy.sh staging deploy

    # Deploy to production with canary
    ./deploy.sh production canary

    # Complete pipeline
    ./deploy.sh all

    # Check status
    ./deploy.sh status

    # Rollback production
    ./deploy.sh production rollback

For more information, see:
    - deployment/local/README.md
    - deployment/staging/README.md
    - deployment/production/README.md
    - DEPLOYMENT_GUIDE.md

EOF
}

# Check prerequisites
check_prerequisites() {
    local env=$1

    if [ "$env" != "local" ]; then
        if [ -z "${GCP_PROJECT_ID:-}" ]; then
            log_error "GCP_PROJECT_ID not set. Please export GCP_PROJECT_ID=your-project-id"
            exit 1
        fi

        if ! command -v gcloud &> /dev/null; then
            log_error "gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install"
            exit 1
        fi
    fi

    if [ "$env" == "local" ]; then
        if ! command -v python3 &> /dev/null; then
            log_error "python3 not found. Please install Python 3.10+"
            exit 1
        fi
    fi
}

# Run local testing (Option C)
run_local() {
    local cmd=${1:-all}

    log_step "Running local testing (Option C)..."
    check_prerequisites "local"

    case "$cmd" in
        setup)
            log_info "Setting up local environment..."
            bash "${SCRIPT_DIR}/deployment/local/setup_local.sh"
            ;;
        integrate)
            log_info "Integrating pilot agents..."
            bash "${SCRIPT_DIR}/deployment/local/integrate_pilot_agents.sh"
            ;;
        test)
            log_info "Testing pilot agents..."
            bash "${SCRIPT_DIR}/deployment/local/test_pilot_agents.sh"
            ;;
        validate)
            log_info "Validating improvements..."
            bash "${SCRIPT_DIR}/deployment/local/validate_improvements.sh"
            ;;
        metrics)
            log_info "Collecting metrics..."
            bash "${SCRIPT_DIR}/deployment/local/collect_metrics.sh"
            ;;
        all)
            log_info "Running complete local testing pipeline..."
            bash "${SCRIPT_DIR}/deployment/local/setup_local.sh"
            bash "${SCRIPT_DIR}/deployment/local/integrate_pilot_agents.sh"
            bash "${SCRIPT_DIR}/deployment/local/test_pilot_agents.sh"
            bash "${SCRIPT_DIR}/deployment/local/validate_improvements.sh"
            bash "${SCRIPT_DIR}/deployment/local/collect_metrics.sh"
            log_success "✓ Local testing complete!"
            ;;
        *)
            log_error "Unknown local command: $cmd"
            log_info "Valid commands: setup, integrate, test, validate, metrics, all"
            exit 1
            ;;
    esac
}

# Run staging deployment (Option A)
run_staging() {
    local cmd=${1:-deploy}

    log_step "Running staging deployment (Option A)..."
    check_prerequisites "staging"

    case "$cmd" in
        setup)
            log_info "Setting up staging environment..."
            bash "${SCRIPT_DIR}/deployment/staging/setup_staging.sh"
            ;;
        deploy)
            log_info "Deploying to staging..."
            bash "${SCRIPT_DIR}/deployment/staging/deploy_pilot_agents.sh"
            ;;
        test)
            log_info "Running smoke tests..."
            bash "${SCRIPT_DIR}/deployment/staging/run_smoke_tests.sh"
            ;;
        validate)
            log_info "Validating staging..."
            bash "${SCRIPT_DIR}/deployment/staging/validate_staging.sh"
            ;;
        rollback)
            log_info "Rolling back staging..."
            bash "${SCRIPT_DIR}/deployment/staging/rollback_staging.sh" "${2:-Manual rollback}"
            ;;
        *)
            log_error "Unknown staging command: $cmd"
            log_info "Valid commands: setup, deploy, test, validate, rollback"
            exit 1
            ;;
    esac
}

# Run production deployment (Option B)
run_production() {
    local cmd=${1:-canary}

    log_step "Running production deployment (Option B)..."
    check_prerequisites "production"

    case "$cmd" in
        setup)
            log_info "Setting up production environment..."
            bash "${SCRIPT_DIR}/deployment/production/setup_production.sh"
            ;;
        blue-green)
            log_info "Deploying with blue-green strategy..."
            bash "${SCRIPT_DIR}/deployment/production/deploy_blue_green.sh"
            ;;
        canary)
            log_info "Deploying with canary strategy..."
            bash "${SCRIPT_DIR}/deployment/production/deploy_canary.sh"
            ;;
        monitor)
            log_info "Starting continuous monitoring..."
            bash "${SCRIPT_DIR}/deployment/production/monitor_production.sh" --continuous
            ;;
        rollback)
            log_info "Rolling back production..."
            bash "${SCRIPT_DIR}/deployment/production/rollback_production.sh"
            ;;
        *)
            log_error "Unknown production command: $cmd"
            log_info "Valid commands: setup, blue-green, canary, monitor, rollback"
            exit 1
            ;;
    esac
}

# Run complete pipeline
run_all() {
    local skip_local=${1:-false}
    local staging_only=${2:-false}

    log_step "Running complete deployment pipeline..."
    echo ""

    # Option C: Local Testing
    if [ "$skip_local" != "true" ]; then
        log_info "═══════════════════════════════════════════"
        log_info "OPTION C: Local Testing"
        log_info "═══════════════════════════════════════════"
        run_local all
        echo ""

        log_info "Review local testing results before proceeding to staging."
        read -p "Continue to staging? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_warn "Deployment stopped at local testing stage."
            exit 0
        fi
    fi

    # Option A: Staging
    log_info "═══════════════════════════════════════════"
    log_info "OPTION A: Staging Deployment"
    log_info "═══════════════════════════════════════════"
    run_staging setup
    run_staging deploy
    run_staging test
    run_staging validate
    log_success "✓ Staging deployment complete!"
    echo ""

    if [ "$staging_only" == "true" ]; then
        log_info "Stopping after staging as requested."
        exit 0
    fi

    log_info "Review staging results before proceeding to production."
    read -p "Continue to PRODUCTION? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warn "Deployment stopped at staging stage."
        exit 0
    fi

    # Option B: Production
    log_info "═══════════════════════════════════════════"
    log_info "OPTION B: Production Deployment"
    log_info "═══════════════════════════════════════════"

    log_info "Select deployment strategy:"
    echo "  1) Blue-Green (zero downtime)"
    echo "  2) Canary (progressive rollout)"
    read -p "Enter choice (1 or 2): " -n 1 -r
    echo

    case $REPLY in
        1)
            run_production blue-green
            ;;
        2)
            run_production canary
            ;;
        *)
            log_error "Invalid choice. Defaulting to canary."
            run_production canary
            ;;
    esac

    log_success "✓ Production deployment complete!"
    echo ""
    log_info "Starting production monitoring..."
    log_info "Press Ctrl+C to stop monitoring (production will continue running)"
    sleep 2
    run_production monitor
}

# Check deployment status
check_status() {
    log_step "Checking deployment status..."
    echo ""

    # Local
    log_info "LOCAL:"
    if [ -d "${SCRIPT_DIR}/deployment/local/pilot_agents" ]; then
        echo "  ✓ Pilot agents integrated"
        if [ -d "${SCRIPT_DIR}/deployment/local/reports" ]; then
            echo "  ✓ Test reports available"
        fi
    else
        echo "  ✗ No local testing done yet"
    fi
    echo ""

    # Staging
    log_info "STAGING:"
    if [ -n "${GCP_PROJECT_ID:-}" ]; then
        if gcloud run services describe agent-improvements-staging \
            --region="${GCP_REGION:-us-central1}" \
            --project="$GCP_PROJECT_ID" &> /dev/null; then
            echo "  ✓ Service deployed"

            url=$(gcloud run services describe agent-improvements-staging \
                --region="${GCP_REGION:-us-central1}" \
                --project="$GCP_PROJECT_ID" \
                --format="get(status.url)")
            echo "  URL: $url"
        else
            echo "  ✗ Not deployed"
        fi
    else
        echo "  ⚠ GCP_PROJECT_ID not set"
    fi
    echo ""

    # Production
    log_info "PRODUCTION:"
    if [ -n "${GCP_PROJECT_ID:-}" ]; then
        if gcloud run services describe agent-improvements-prod \
            --region="${GCP_REGION:-us-central1}" \
            --project="$GCP_PROJECT_ID" &> /dev/null; then
            echo "  ✓ Service deployed"

            url=$(gcloud run services describe agent-improvements-prod \
                --region="${GCP_REGION:-us-central1}" \
                --project="$GCP_PROJECT_ID" \
                --format="get(status.url)")
            echo "  URL: $url"

            # Traffic split
            traffic=$(gcloud run services describe agent-improvements-prod \
                --region="${GCP_REGION:-us-central1}" \
                --project="$GCP_PROJECT_ID" \
                --format="get(status.traffic)")
            echo "  Traffic: $traffic"
        else
            echo "  ✗ Not deployed"
        fi
    else
        echo "  ⚠ GCP_PROJECT_ID not set"
    fi
}

# Main
main() {
    print_banner

    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    local command=$1
    shift

    case "$command" in
        local)
            run_local "$@"
            ;;
        staging)
            run_staging "$@"
            ;;
        production)
            run_production "$@"
            ;;
        all)
            run_all "$@"
            ;;
        status)
            check_status
            ;;
        rollback)
            if [ $# -eq 0 ]; then
                log_error "Rollback requires --env flag (staging or production)"
                exit 1
            fi
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
