#!/bin/bash
# Staging Environment Setup Script
# Creates all GCP resources needed for staging deployment

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
ENVIRONMENT="staging"
SERVICE_NAME="agent-improvements-staging"

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

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

    log_info "Prerequisites check passed ✓"
}

# Set active project
set_project() {
    log_info "Setting active project to: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"
}

# Enable required APIs
enable_apis() {
    log_info "Enabling required GCP APIs..."

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
    )

    for api in "${apis[@]}"; do
        log_info "Enabling $api..."
        gcloud services enable "$api" --project="$PROJECT_ID" 2>/dev/null || log_warn "$api already enabled"
    done

    log_info "APIs enabled ✓"
}

# Create service account
create_service_account() {
    log_info "Creating service account for staging..."

    local sa_name="agent-staging"
    local sa_email="${sa_name}@${PROJECT_ID}.iam.gserviceaccount.com"

    if gcloud iam service-accounts describe "$sa_email" --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Service account $sa_email already exists"
    else
        gcloud iam service-accounts create "$sa_name" \
            --display-name="Agent Improvements Staging Service Account" \
            --project="$PROJECT_ID"
        log_info "Service account created ✓"
    fi

    # Grant necessary roles
    log_info "Granting IAM roles..."
    local roles=(
        "roles/aiplatform.user"
        "roles/logging.logWriter"
        "roles/cloudtrace.agent"
        "roles/monitoring.metricWriter"
        "roles/secretmanager.secretAccessor"
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

# Create Redis instance for staging
create_redis() {
    log_info "Creating Redis instance for staging..."

    local redis_name="agent-cache-staging"

    if gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Redis instance $redis_name already exists"
        REDIS_HOST=$(gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" --format="get(host)")
        log_info "Redis host: $REDIS_HOST"
    else
        log_info "Creating Redis instance (this may take 5-10 minutes)..."
        gcloud redis instances create "$redis_name" \
            --size=1 \
            --region="$REGION" \
            --redis-version=redis_7_0 \
            --tier=basic \
            --project="$PROJECT_ID"

        REDIS_HOST=$(gcloud redis instances describe "$redis_name" --region="$REGION" --project="$PROJECT_ID" --format="get(host)")
        log_info "Redis instance created ✓"
        log_info "Redis host: $REDIS_HOST"
    fi
}

# Create secrets in Secret Manager
create_secrets() {
    log_info "Setting up Secret Manager..."

    # Create Redis URL secret
    if gcloud secrets describe redis-url --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Secret redis-url already exists"
    else
        echo -n "redis://${REDIS_HOST}:6379" | gcloud secrets create redis-url \
            --data-file=- \
            --replication-policy="automatic" \
            --project="$PROJECT_ID"
        log_info "Redis URL secret created ✓"
    fi

    # Create staging environment config
    if gcloud secrets describe staging-config --project="$PROJECT_ID" &> /dev/null; then
        log_warn "Secret staging-config already exists"
    else
        cat > /tmp/staging-config.yaml << EOF
environment: staging
enable_debug: false
cost_tracking:
  enabled: true
  budgets:
    daily: 100
    monthly: 2500
observability:
  sampling_rate: 1.0
  cloud_logging: true
  cloud_trace: true
EOF
        gcloud secrets create staging-config \
            --data-file=/tmp/staging-config.yaml \
            --replication-policy="automatic" \
            --project="$PROJECT_ID"
        rm /tmp/staging-config.yaml
        log_info "Staging config secret created ✓"
    fi
}

# Build container image
build_image() {
    log_info "Building container image for staging..."

    # Create Dockerfile if it doesn't exist
    if [ ! -f "Dockerfile" ]; then
        log_info "Creating Dockerfile..."
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

    # Build with Cloud Build
    log_info "Submitting build to Cloud Build..."
    gcloud builds submit \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest" \
        --tag "gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S)" \
        --project="$PROJECT_ID" \
        .

    log_info "Container image built ✓"
}

# Deploy to Cloud Run
deploy_to_cloud_run() {
    log_info "Deploying to Cloud Run (staging)..."

    local sa_email="agent-staging@${PROJECT_ID}.iam.gserviceaccount.com"

    gcloud run deploy "$SERVICE_NAME" \
        --image="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest" \
        --platform=managed \
        --region="$REGION" \
        --service-account="$sa_email" \
        --memory=2Gi \
        --cpu=2 \
        --timeout=300 \
        --concurrency=100 \
        --min-instances=0 \
        --max-instances=5 \
        --set-env-vars="ENVIRONMENT=staging,LOG_LEVEL=INFO,GCP_PROJECT_ID=${PROJECT_ID}" \
        --set-secrets="REDIS_URL=redis-url:latest,STAGING_CONFIG=staging-config:latest" \
        --allow-unauthenticated \
        --project="$PROJECT_ID"

    # Get service URL
    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)")

    log_info "Staging deployment complete ✓"
    log_info "Service URL: $SERVICE_URL"
}

# Create monitoring dashboard
create_dashboard() {
    log_info "Creating Cloud Monitoring dashboard..."

    cat > /tmp/staging-dashboard.json << EOF
{
  "displayName": "Agent Improvements - Staging",
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
                  "filter": "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${SERVICE_NAME}\"",
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
                  "filter": "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"${SERVICE_NAME}\" metric.type=\"run.googleapis.com/request_count\" metric.labels.response_code_class=\"5xx\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
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

    # Note: Creating dashboards via gcloud is limited, user may need to import manually
    log_info "Dashboard configuration saved to /tmp/staging-dashboard.json"
    log_info "Import manually at: https://console.cloud.google.com/monitoring/dashboards"
}

# Summary
print_summary() {
    log_info ""
    log_info "=========================================="
    log_info "STAGING SETUP COMPLETE ✓"
    log_info "=========================================="
    log_info ""
    log_info "Project: $PROJECT_ID"
    log_info "Region: $REGION"
    log_info "Service URL: $SERVICE_URL"
    log_info "Redis Host: ${REDIS_HOST:-Not created}"
    log_info ""
    log_info "Next steps:"
    log_info "1. Run smoke tests: ./deployment/staging/run_smoke_tests.sh"
    log_info "2. Deploy pilot agents: ./deployment/staging/deploy_pilot_agents.sh"
    log_info "3. Validate metrics: ./deployment/staging/validate_staging.sh"
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
    log_info "Starting staging environment setup..."
    log_info ""

    check_prerequisites
    set_project
    enable_apis
    create_service_account
    create_redis
    create_secrets
    build_image
    deploy_to_cloud_run
    create_dashboard
    print_summary
}

# Run main function
main "$@"
