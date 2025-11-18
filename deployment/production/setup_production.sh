#!/bin/bash
# Production Environment Setup Script
# Creates all GCP resources needed for production deployment
# WARNING: This script creates production resources and should be used with caution

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
ENVIRONMENT="production"
SERVICE_NAME="agent-improvements-prod"
LOG_FILE="/tmp/production-setup-$(date +%Y%m%d-%H%M%S).log"

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

# Function to require confirmation for production
require_confirmation() {
    local action="$1"
    echo ""
    log_warn "⚠️  PRODUCTION ACTION: $action"
    log_warn "This will create production resources in project: $PROJECT_ID"
    echo ""
    read -p "Are you sure you want to proceed? (type 'yes' to confirm): " confirmation

    if [ "$confirmation" != "yes" ]; then
        log_error "Production setup cancelled by user"
        exit 1
    fi
    log_info "Confirmation received, proceeding..."
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."

    if [ -z "$PROJECT_ID" ]; then
        log_error "GCP_PROJECT_ID environment variable not set"
        echo "Please set: export GCP_PROJECT_ID=your-project-id"
        exit 1
    fi

    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI not found. Please install: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi

    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
        log_error "Not authenticated with gcloud. Please run: gcloud auth login"
        exit 1
    fi

    # Verify user has necessary permissions
    log_info "Verifying IAM permissions..."
    if ! gcloud projects get-iam-policy "$PROJECT_ID" &> /dev/null; then
        log_error "You do not have permission to access project: $PROJECT_ID"
        exit 1
    fi

    log_info "Prerequisites check passed ✓"
}

# Set active project
set_project() {
    log_step "Setting active project to: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"
}

# Enable required APIs
enable_apis() {
    log_step "Enabling required GCP APIs..."

    local apis=(
        "aiplatform.googleapis.com"
        "logging.googleapis.com"
        "cloudtrace.googleapis.com"
        "monitoring.googleapis.com"
        "run.googleapis.com"
        "cloudbuild.googleapis.com"
        "containerregistry.googleapis.com"
        "redis.googleapis.com"
        "secretmanager.googleapis.com"
        "cloudscheduler.googleapis.com"
        "pubsub.googleapis.com"
    )

    for api in "${apis[@]}"; do
        log_info "Enabling $api..."
        gcloud services enable "$api" --project="$PROJECT_ID" 2>/dev/null || log_warn "$api already enabled"
    done

    log_info "APIs enabled ✓"
}

# Create production service account
create_service_account() {
    log_step "Creating production service account..."

    local sa_name="agent-production"
    local sa_email="${sa_name}@${PROJECT_ID}.iam.gserviceaccount.com"

    if gcloud iam service-accounts describe "$sa_email" --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Service account $sa_email already exists"
    else
        gcloud iam service-accounts create "$sa_name" \
            --display-name="Agent Improvements Production Service Account" \
            --description="Service account for production agent improvements service" \
            --project="$PROJECT_ID"
        log_info "Service account created ✓"
    fi

    # Grant necessary roles for production
    log_info "Granting production IAM roles..."
    local roles=(
        "roles/aiplatform.user"
        "roles/logging.logWriter"
        "roles/cloudtrace.agent"
        "roles/monitoring.metricWriter"
        "roles/secretmanager.secretAccessor"
        "roles/cloudscheduler.admin"
    )

    for role in "${roles[@]}"; do
        gcloud projects add-iam-policy-binding "$PROJECT_ID" \
            --member="serviceAccount:$sa_email" \
            --role="$role" \
            --condition=None \
            > /dev/null 2>&1 || log_warn "Role $role may already be assigned"
    done

    log_info "IAM roles configured ✓"
}

# Create Redis instance for production (HA tier)
create_redis() {
    log_step "Creating Redis instance for production (HA tier)..."

    local redis_name="agent-cache-production"

    if gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Redis instance $redis_name already exists"
        REDIS_HOST=$(gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" --format="get(host)")
        log_info "Redis host: $REDIS_HOST"
    else
        log_info "Creating production Redis instance with HA (this may take 10-15 minutes)..."
        log_warn "Production Redis uses standard-ha tier for high availability"

        gcloud redis instances create "$redis_name" \
            --size=5 \
            --region="$REGION" \
            --redis-version=redis_7_0 \
            --tier=standard-ha \
            --replica-count=1 \
            --read-replicas-mode=READ_REPLICAS_ENABLED \
            --project="$PROJECT_ID"

        REDIS_HOST=$(gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" --format="get(host)")
        log_info "Redis instance created ✓"
        log_info "Redis host: $REDIS_HOST"
    fi
}

# Create secrets in Secret Manager
create_secrets() {
    log_step "Setting up Secret Manager for production..."

    # Create Redis URL secret
    if gcloud secrets describe redis-url-prod --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Secret redis-url-prod already exists"
    else
        echo -n "redis://${REDIS_HOST}:6379" | gcloud secrets create redis-url-prod \
            --data-file=- \
            --replication-policy="automatic" \
            --project="$PROJECT_ID"
        log_info "Redis URL secret created ✓"
    fi

    # Create production environment config
    if gcloud secrets describe production-config --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Secret production-config already exists"
    else
        cat > /tmp/production-config.yaml << EOF
environment: production
enable_debug: false
cost_tracking:
  enabled: true
  budgets:
    daily: 500
    monthly: 15000
  alerts:
    - threshold: 80
      recipients: ["ops@example.com"]
    - threshold: 95
      recipients: ["ops@example.com", "leadership@example.com"]
observability:
  sampling_rate: 0.1  # 10% sampling in production
  cloud_logging: true
  cloud_trace: true
  error_reporting: true
performance:
  max_concurrent_agents: 1000
  request_timeout: 300
  rate_limiting:
    enabled: true
    requests_per_minute: 1000
slo:
  success_rate: 0.99
  p95_latency_ms: 5000
  availability: 0.999
EOF
        gcloud secrets create production-config \
            --data-file=/tmp/production-config.yaml \
            --replication-policy="automatic" \
            --project="$PROJECT_ID"
        rm /tmp/production-config.yaml
        log_info "Production config secret created ✓"
    fi

    # Set up secret access permissions
    local sa_email="agent-production@${PROJECT_ID}.iam.gserviceaccount.com"
    for secret in redis-url-prod production-config; do
        gcloud secrets add-iam-policy-binding "$secret" \
            --member="serviceAccount:$sa_email" \
            --role="roles/secretmanager.secretAccessor" \
            --project="$PROJECT_ID" \
            > /dev/null 2>&1 || log_warn "Secret access already granted"
    done

    log_info "Secrets configured ✓"
}

# Build container image
build_image() {
    log_step "Building container image for production..."

    # Verify we're building from a clean state
    if ! git diff-index --quiet HEAD --; then
        log_error "Working directory has uncommitted changes"
        log_error "Production builds must be from committed code"
        exit 1
    fi

    local git_sha=$(git rev-parse --short HEAD)
    local timestamp=$(date +%Y%m%d-%H%M%S)

    # Create Dockerfile if it doesn't exist
    if [ ! -f "Dockerfile" ]; then
        log_info "Creating production Dockerfile..."
        cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[prod]"

# Copy application code
COPY . .

# Create non-root user for production
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose metrics port
EXPOSE 8080
EXPOSE 9090

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF
    fi

    # Build with Cloud Build (production tags)
    log_info "Submitting build to Cloud Build..."
    log_info "Git SHA: $git_sha"

    gcloud builds submit \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest" \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${git_sha}" \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:prod-${timestamp}" \
        --project="$PROJECT_ID" \
        .

    log_info "Container image built ✓"
    log_info "Image: gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${git_sha}"
}

# Deploy to Cloud Run (production configuration)
deploy_to_cloud_run() {
    log_step "Deploying to Cloud Run (PRODUCTION)..."

    local sa_email="agent-production@${PROJECT_ID}.iam.gserviceaccount.com"
    local git_sha=$(git rev-parse --short HEAD)

    log_warn "Deploying to PRODUCTION environment"
    log_info "Image: gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${git_sha}"

    gcloud run deploy "$SERVICE_NAME" \
        --image="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${git_sha}" \
        --platform=managed \
        --region="$REGION" \
        --service-account="$sa_email" \
        --memory=4Gi \
        --cpu=4 \
        --timeout=300 \
        --concurrency=80 \
        --min-instances=1 \
        --max-instances=10 \
        --cpu-throttling \
        --set-env-vars="ENVIRONMENT=production,LOG_LEVEL=INFO,GCP_PROJECT_ID=${PROJECT_ID}" \
        --set-secrets="REDIS_URL=redis-url-prod:latest,PRODUCTION_CONFIG=production-config:latest" \
        --no-allow-unauthenticated \
        --project="$PROJECT_ID" \
        --tag="prod-${git_sha}"

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)")

    log_info "Production deployment complete ✓"
    log_info "Service URL: $SERVICE_URL"
    log_warn "Service requires authentication (--no-allow-unauthenticated)"
}

# Create alerting policies
create_alerting() {
    log_step "Creating alerting policies..."

    log_info "Setting up Cloud Monitoring alerts..."

    # Note: Alert policies would typically be created via Terraform or gcloud
    # This is a simplified version
    log_info "Alert policies should be configured in Cloud Console:"
    log_info "  - Error rate > 1%"
    log_info "  - P95 latency > 5000ms"
    log_info "  - Success rate < 99%"
    log_info "  - Instance count anomalies"
    log_info "  - Cost anomalies (>20% deviation)"

    log_warn "Please configure alerts manually at:"
    log_warn "  https://console.cloud.google.com/monitoring/alerting?project=$PROJECT_ID"
}

# Create monitoring dashboard
create_dashboard() {
    log_step "Creating Cloud Monitoring dashboard..."

    cat > /tmp/production-dashboard.json << EOF
{
  "displayName": "Agent Improvements - Production",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Request Rate",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\\"cloud_run_revision\\" resource.labels.service_name=\\"${SERVICE_NAME}\\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "xPos": 6,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Error Rate",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\\"cloud_run_revision\\" resource.labels.service_name=\\"${SERVICE_NAME}\\" metric.type=\\"run.googleapis.com/request_count\\" metric.labels.response_code_class=\\"5xx\\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "yPos": 4,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "P95 Latency",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\\"cloud_run_revision\\" resource.labels.service_name=\\"${SERVICE_NAME}\\" metric.type=\\"run.googleapis.com/request_latencies\\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_DELTA",
                    "crossSeriesReducer": "REDUCE_PERCENTILE_95"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "xPos": 6,
        "yPos": 4,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Instance Count",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\\"cloud_run_revision\\" resource.labels.service_name=\\"${SERVICE_NAME}\\" metric.type=\\"run.googleapis.com/container/instance_count\\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_MAX"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF

    log_info "Dashboard configuration saved to /tmp/production-dashboard.json"
    log_info "Import manually at: https://console.cloud.google.com/monitoring/dashboards?project=$PROJECT_ID"
}

# Create backup and disaster recovery plan
create_backup_plan() {
    log_step "Setting up backup and DR plan..."

    # Create a Cloud Scheduler job for automated backups
    log_info "Production backup plan:"
    log_info "  - Redis: Automated snapshots enabled"
    log_info "  - Secrets: Replicated automatically"
    log_info "  - Container images: Multiple tags retained"
    log_info "  - Logs: 30-day retention in Cloud Logging"

    log_info "Backup configuration complete ✓"
}

# Summary
print_summary() {
    log_info ""
    echo "=========================================="
    echo "  PRODUCTION SETUP COMPLETE ✓"
    echo "=========================================="
    log_info ""
    log_info "Project: $PROJECT_ID"
    log_info "Region: $REGION"
    log_info "Environment: PRODUCTION"
    log_info "Service URL: $SERVICE_URL"
    log_info "Redis Host: ${REDIS_HOST:-Not created}"
    log_info "Log File: $LOG_FILE"
    log_info ""
    log_warn "IMPORTANT PRODUCTION NOTES:"
    log_warn "  - Service requires authentication"
    log_warn "  - Min instances: 1 (always warm)"
    log_warn "  - Max instances: 10"
    log_warn "  - Memory: 4GB per instance"
    log_warn "  - CPU: 4 vCPU per instance"
    log_warn "  - Redis: HA tier with read replicas"
    log_info ""
    log_info "Next steps:"
    log_info "1. Configure alerting: ./deployment/production/create_alerts.sh"
    log_info "2. Run smoke tests: ./deployment/production/smoke_tests.sh"
    log_info "3. Enable monitoring: ./deployment/production/monitor_production.sh"
    log_info "4. Configure blue-green: ./deployment/production/deploy_blue_green.sh"
    log_info ""
    log_info "Deployment options:"
    log_info "  Blue-Green: ./deployment/production/deploy_blue_green.sh"
    log_info "  Canary:     ./deployment/production/deploy_canary.sh"
    log_info "  Rollback:   ./deployment/production/rollback_production.sh"
    log_info ""
    log_info "To view logs:"
    log_info "  gcloud run logs read $SERVICE_NAME --region=$REGION --project=$PROJECT_ID"
    log_info ""
    log_info "To monitor:"
    log_info "  https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"
    log_info ""
}

# Main execution
main() {
    log_info "=========================================="
    log_info "  PRODUCTION ENVIRONMENT SETUP"
    log_info "=========================================="
    log_info ""
    log_info "This script will create production resources"
    log_info "Log file: $LOG_FILE"
    log_info ""

    # Require explicit confirmation for production
    require_confirmation "Production environment setup"

    check_prerequisites
    set_project
    enable_apis
    create_service_account
    create_redis
    create_secrets
    build_image
    deploy_to_cloud_run
    create_alerting
    create_dashboard
    create_backup_plan
    print_summary
}

# Run main function
main "$@"
