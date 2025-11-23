#!/bin/bash
#
# Deploy Agent to Google Cloud Run
#
# Usage: ./deploy_agent.sh <agent_name>
#

set -e

if [ -z "$1" ]; then
    echo "Usage: ./deploy_agent.sh <agent_name>"
    echo "Example: ./deploy_agent.sh ceo"
    exit 1
fi

AGENT_NAME=$1
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"mapache-a2a"}
REGION=${REGION:-"us-central1"}
REGISTRY_URL=${A2A_REGISTRY_URL:-"https://registry.mapache.ai"}

echo "========================================="
echo "Deploying Agent: ${AGENT_NAME}"
echo "========================================="
echo ""
echo "Project:  ${PROJECT_ID}"
echo "Region:   ${REGION}"
echo "Registry: ${REGISTRY_URL}"
echo ""

# Create Dockerfile for the agent
cat > Dockerfile.agent <<EOF
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/ agents/
COPY infrastructure/ infrastructure/

# Set environment variables
ENV PYTHONPATH=/app
ENV AGENT_NAME=${AGENT_NAME}
ENV PORT=8080

# Run the agent server
CMD python -m agents.${AGENT_NAME}.agent
EOF

# Build the container
echo "Building container image..."
gcloud builds submit \
    --tag gcr.io/${PROJECT_ID}/agent-${AGENT_NAME} \
    --project ${PROJECT_ID}

# Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy agent-${AGENT_NAME} \
    --image gcr.io/${PROJECT_ID}/agent-${AGENT_NAME} \
    --platform managed \
    --region ${REGION} \
    --project ${PROJECT_ID} \
    --allow-unauthenticated \
    --set-env-vars="A2A_REGISTRY_URL=${REGISTRY_URL},ENVIRONMENT=production"

# Get the service URL
SERVICE_URL=$(gcloud run services describe agent-${AGENT_NAME} \
    --platform managed \
    --region ${REGION} \
    --project ${PROJECT_ID} \
    --format 'value(status.url)')

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Agent URL: ${SERVICE_URL}"
echo "Agent Card: ${SERVICE_URL}/.well-known/agent.json"
echo "Health Check: ${SERVICE_URL}/health"
echo ""

# Register agent with central registry
echo "Registering agent with central registry..."
curl -X POST "${REGISTRY_URL}/agents/register" \
    -H "Authorization: Bearer ${BEARER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"${AGENT_NAME}\",
        \"url\": \"${SERVICE_URL}\"
    }"

echo ""
echo "Agent ${AGENT_NAME} deployed and registered successfully!"
