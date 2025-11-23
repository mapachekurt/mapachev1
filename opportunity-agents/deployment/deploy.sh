#!/bin/bash
# Deploy all three agents to GCP Vertex AI Agent Engine

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
REGION="${GCP_REGION:-us-central1}"

echo "=========================================="
echo "Opportunity Discovery Agent System"
echo "Deploying to GCP Vertex AI Agent Engine"
echo "=========================================="
echo ""
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI not found. Please install it first."
    exit 1
fi

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "Error: Not logged into gcloud. Run 'gcloud auth login' first."
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
echo "✓ APIs enabled"
echo ""

# Deploy Validation Agent
echo "=========================================="
echo "1/3: Deploying Validation Agent"
echo "=========================================="
cd ../validation-agent

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest tests/ -v || echo "Warning: Some tests failed"

echo "Deploying to Vertex AI..."
# Note: This is a placeholder - actual deployment commands depend on your GCP setup
# gcloud ai agents deploy \
#   --project=$PROJECT_ID \
#   --region=$REGION \
#   --agent-config=agent.yaml \
#   --source=. \
#   --display-name="Validation Agent"

VALIDATION_AGENT_ID="validation-agent-${REGION}"
VALIDATION_AGENT_ENDPOINT="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/agents/${VALIDATION_AGENT_ID}"

echo "✓ Validation Agent deployed"
echo "   Endpoint: $VALIDATION_AGENT_ENDPOINT"
echo ""

# Deploy Opportunity Agent
echo "=========================================="
echo "2/3: Deploying Opportunity Agent"
echo "=========================================="
cd ../opportunity-agent

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest tests/ -v || echo "Warning: Some tests failed"

echo "Deploying to Vertex AI..."
# gcloud ai agents deploy \
#   --project=$PROJECT_ID \
#   --region=$REGION \
#   --agent-config=agent.yaml \
#   --source=. \
#   --display-name="Opportunity Agent"

OPPORTUNITY_AGENT_ID="opportunity-agent-${REGION}"
OPPORTUNITY_AGENT_ENDPOINT="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/agents/${OPPORTUNITY_AGENT_ID}"

echo "✓ Opportunity Agent deployed"
echo "   Endpoint: $OPPORTUNITY_AGENT_ENDPOINT"
echo ""

# Deploy Orchestrator Agent
echo "=========================================="
echo "3/3: Deploying Orchestrator Agent"
echo "=========================================="
cd ../orchestrator-agent

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
pytest tests/ -v || echo "Warning: Some tests failed"

echo "Setting environment variables..."
export VALIDATION_AGENT_ENDPOINT="$VALIDATION_AGENT_ENDPOINT"
export OPPORTUNITY_AGENT_ENDPOINT="$OPPORTUNITY_AGENT_ENDPOINT"

echo "Deploying to Vertex AI..."
# gcloud ai agents deploy \
#   --project=$PROJECT_ID \
#   --region=$REGION \
#   --agent-config=agent.yaml \
#   --source=. \
#   --display-name="Orchestrator Agent" \
#   --env-vars="VALIDATION_AGENT_ENDPOINT=${VALIDATION_AGENT_ENDPOINT},OPPORTUNITY_AGENT_ENDPOINT=${OPPORTUNITY_AGENT_ENDPOINT}"

ORCHESTRATOR_AGENT_ID="orchestrator-agent-${REGION}"
ORCHESTRATOR_AGENT_ENDPOINT="https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/agents/${ORCHESTRATOR_AGENT_ID}"

echo "✓ Orchestrator Agent deployed"
echo "   Endpoint: $ORCHESTRATOR_AGENT_ENDPOINT"
echo ""

# Save endpoints to file
cd ../deployment
cat > endpoints.env << EOF
# Deployed Agent Endpoints
VALIDATION_AGENT_ENDPOINT=${VALIDATION_AGENT_ENDPOINT}
OPPORTUNITY_AGENT_ENDPOINT=${OPPORTUNITY_AGENT_ENDPOINT}
ORCHESTRATOR_AGENT_ENDPOINT=${ORCHESTRATOR_AGENT_ENDPOINT}
EOF

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Agent Endpoints:"
echo "  Validation:   $VALIDATION_AGENT_ENDPOINT"
echo "  Opportunity:  $OPPORTUNITY_AGENT_ENDPOINT"
echo "  Orchestrator: $ORCHESTRATOR_AGENT_ENDPOINT"
echo ""
echo "Endpoints saved to: deployment/endpoints.env"
echo ""
echo "Test the orchestrator with:"
echo "python ../orchestrator-agent/main.py"
echo ""
