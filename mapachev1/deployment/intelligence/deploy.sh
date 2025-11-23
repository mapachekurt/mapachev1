#!/bin/bash
# Deployment script for Mapache Intelligence System
#
# Usage: ./deploy.sh [OPTIONS]
# Options:
#   --project PROJECT_ID    GCP project ID (default: mapache-intelligence-prod)
#   --region REGION         GCP region (default: europe-west1)
#   --skip-build           Skip building Docker images
#   --skip-infrastructure  Skip infrastructure setup
#   --help                 Show this help message

set -e

# Default values
PROJECT_ID="${GCP_PROJECT_ID:-mapache-intelligence-prod}"
REGION="${GCP_REGION:-europe-west1}"
SKIP_BUILD=false
SKIP_INFRA=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --project)
      PROJECT_ID="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --skip-infrastructure)
      SKIP_INFRA=true
      shift
      ;;
    --help)
      grep "^#" "$0" | cut -c 3-
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "============================================"
echo "Mapache Intelligence System Deployment"
echo "============================================"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Set gcloud project
gcloud config set project "$PROJECT_ID"

# Phase 1: Enable Required APIs
if [ "$SKIP_INFRA" = false ]; then
  echo "[1/10] Enabling required GCP APIs..."
  gcloud services enable \
    run.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudbuild.googleapis.com \
    cloudscheduler.googleapis.com \
    workflows.googleapis.com \
    eventarc.googleapis.com \
    pubsub.googleapis.com \
    firestore.googleapis.com \
    storage.googleapis.com \
    aiplatform.googleapis.com \
    secretmanager.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com
fi

# Phase 2: Create Pub/Sub Topics
if [ "$SKIP_INFRA" = false ]; then
  echo "[2/10] Creating Pub/Sub topics..."

  # Create topics
  gcloud pubsub topics create intelligence-raw-content --project="$PROJECT_ID" || true
  gcloud pubsub topics create intelligence-analyzed-content --project="$PROJECT_ID" || true
  gcloud pubsub topics create intelligence-dead-letter --project="$PROJECT_ID" || true

  # Create subscriptions
  gcloud pubsub subscriptions create intelligence-raw-content-sub \
    --topic=intelligence-raw-content \
    --ack-deadline=60 \
    --dead-letter-topic=intelligence-dead-letter \
    --max-delivery-attempts=5 \
    --project="$PROJECT_ID" || true
fi

# Phase 3: Create GCS Bucket
if [ "$SKIP_INFRA" = false ]; then
  echo "[3/10] Creating GCS bucket..."
  gsutil mb -p "$PROJECT_ID" -c STANDARD -l "$REGION" \
    gs://mapache-intelligence-raw-content || true

  # Set lifecycle policy (delete after 90 days)
  echo '{
    "lifecycle": {
      "rule": [{
        "action": {"type": "Delete"},
        "condition": {"age": 90}
      }]
    }
  }' > /tmp/lifecycle.json

  gsutil lifecycle set /tmp/lifecycle.json \
    gs://mapache-intelligence-raw-content || true
fi

# Phase 4: Create Firestore Database
if [ "$SKIP_INFRA" = false ]; then
  echo "[4/10] Setting up Firestore..."
  gcloud firestore databases create \
    --location="$REGION" \
    --type=firestore-native \
    --project="$PROJECT_ID" || true
fi

# Phase 5: Configure Secret Manager
if [ "$SKIP_INFRA" = false ]; then
  echo "[5/10] Configuring Secret Manager..."

  # Create secrets (with placeholder values - update later)
  echo -n "PLACEHOLDER_LINEAR_API_KEY" | \
    gcloud secrets create linear-api-key \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true

  echo -n "PLACEHOLDER_SLACK_WEBHOOK" | \
    gcloud secrets create slack-webhook-url \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true

  echo -n "PLACEHOLDER_REDDIT_CLIENT_ID" | \
    gcloud secrets create reddit-client-id \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true

  echo -n "PLACEHOLDER_REDDIT_CLIENT_SECRET" | \
    gcloud secrets create reddit-client-secret \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true

  echo -n "PLACEHOLDER_GITHUB_TOKEN" | \
    gcloud secrets create github-token \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true

  echo -n "PLACEHOLDER_PRODUCTHUNT_TOKEN" | \
    gcloud secrets create producthunt-api-token \
    --data-file=- \
    --replication-policy="automatic" \
    --project="$PROJECT_ID" || true
fi

# Phase 6: Build and Push Docker Images
if [ "$SKIP_BUILD" = false ]; then
  echo "[6/10] Building and pushing Docker images..."

  SCRAPERS=("hackernews" "reddit" "producthunt" "blogs" "arxiv" "github")

  cd mapachev1

  for scraper in "${SCRAPERS[@]}"; do
    echo "Building $scraper scraper..."

    gcloud builds submit \
      --tag="gcr.io/$PROJECT_ID/intelligence-scraper-$scraper:latest" \
      --dockerfile="deployment/intelligence/cloud_run/Dockerfile.$scraper" \
      --project="$PROJECT_ID" \
      .
  done

  cd ..
fi

# Phase 7: Deploy Cloud Run Jobs
echo "[7/10] Deploying Cloud Run Jobs..."

SCRAPERS=("hackernews" "reddit" "producthunt" "blogs" "arxiv" "github")

for scraper in "${SCRAPERS[@]}"; do
  echo "Deploying $scraper Cloud Run Job..."

  gcloud run jobs create "intelligence-scraper-$scraper" \
    --image="gcr.io/$PROJECT_ID/intelligence-scraper-$scraper:latest" \
    --region="$REGION" \
    --max-retries=2 \
    --task-timeout=10m \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=$REGION" \
    --project="$PROJECT_ID" || \
  gcloud run jobs update "intelligence-scraper-$scraper" \
    --image="gcr.io/$PROJECT_ID/intelligence-scraper-$scraper:latest" \
    --region="$REGION" \
    --project="$PROJECT_ID"
done

# Phase 8: Deploy Cloud Functions
echo "[8/10] Deploying Cloud Functions..."

cd mapachev1

# Deploy analyzer function
gcloud functions deploy intelligence-content-analyzer \
  --gen2 \
  --runtime=python311 \
  --region="$REGION" \
  --source=. \
  --entry-point=analyze_content \
  --trigger-topic=intelligence-raw-content \
  --timeout=300s \
  --memory=512MB \
  --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
  --project="$PROJECT_ID"

# Deploy chief agent function
gcloud functions deploy intelligence-chief-agent \
  --gen2 \
  --runtime=python311 \
  --region="$REGION" \
  --source=. \
  --entry-point=trigger_daily_briefing \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=1GB \
  --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
  --project="$PROJECT_ID"

cd ..

# Phase 9: Deploy Cloud Workflows
echo "[9/10] Deploying Cloud Workflows..."

gcloud workflows deploy intelligence-orchestrator \
  --source=mapachev1/deployment/intelligence/workflows/intelligence-orchestrator.yaml \
  --location="$REGION" \
  --project="$PROJECT_ID"

# Phase 10: Set up Cloud Scheduler
echo "[10/10] Setting up Cloud Scheduler..."

# Scraping job - every 30 minutes
gcloud scheduler jobs create http scraping-orchestrator \
  --location="$REGION" \
  --schedule="*/30 * * * *" \
  --uri="https://workflowexecutions.googleapis.com/v1/projects/$PROJECT_ID/locations/$REGION/workflows/intelligence-orchestrator/executions" \
  --oauth-service-account-email="$PROJECT_ID@appspot.gserviceaccount.com" \
  --time-zone="Europe/Paris" \
  --project="$PROJECT_ID" || \
gcloud scheduler jobs update http scraping-orchestrator \
  --location="$REGION" \
  --schedule="*/30 * * * *" \
  --project="$PROJECT_ID"

# Chief agent job - daily at 6 AM CET
CHIEF_AGENT_URL=$(gcloud functions describe intelligence-chief-agent \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --format="value(serviceConfig.uri)")

gcloud scheduler jobs create http chief-agent-daily-trigger \
  --location="$REGION" \
  --schedule="0 6 * * *" \
  --uri="$CHIEF_AGENT_URL" \
  --http-method=POST \
  --time-zone="Europe/Paris" \
  --project="$PROJECT_ID" || \
gcloud scheduler jobs update http chief-agent-daily-trigger \
  --location="$REGION" \
  --schedule="0 6 * * *" \
  --project="$PROJECT_ID"

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Update Secret Manager with real API keys:"
echo "   - linear-api-key"
echo "   - slack-webhook-url"
echo "   - reddit-client-id"
echo "   - reddit-client-secret"
echo "   - github-token"
echo "   - producthunt-api-token"
echo ""
echo "2. Test the system:"
echo "   gcloud workflows execute intelligence-orchestrator --location=$REGION"
echo ""
echo "3. Monitor logs:"
echo "   gcloud logging read 'resource.type=cloud_run_job' --limit=50"
echo ""
echo "4. Cloud Scheduler jobs are created but PAUSED. Enable them when ready:"
echo "   gcloud scheduler jobs resume scraping-orchestrator --location=$REGION"
echo "   gcloud scheduler jobs resume chief-agent-daily-trigger --location=$REGION"
echo ""
