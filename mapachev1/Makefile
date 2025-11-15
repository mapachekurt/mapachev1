# ==============================================================================
# Installation & Setup
# ==============================================================================

# Install dependencies using uv package manager
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.8.13/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync

# ==============================================================================
# Playground Targets
# ==============================================================================

# Launch local dev playground
playground:
	@echo "==============================================================================="
	@echo "| 🚀 Starting your agent playground...                                        |"
	@echo "|                                                                             |"
	@echo "| 💡 Try asking: What's the weather in San Francisco?                         |"
	@echo "|                                                                             |"
	@echo "| 🔍 IMPORTANT: Select the 'app' folder to interact with your agent.          |"
	@echo "==============================================================================="
	uv run adk web . --port 8501 --reload_agents

# ==============================================================================
# Backend Deployment Targets
# ==============================================================================

# Deploy the agent remotely
deploy:
	# Export dependencies to requirements file using uv export.
	(uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > app/app_utils/.requirements.txt 2>/dev/null || \
	uv export --no-hashes --no-header --no-dev --no-emit-project > app/app_utils/.requirements.txt) && \
	uv run -m app.app_utils.deploy \
		--source-packages=./app \
		--entrypoint-module=app.agent_engine_app \
		--entrypoint-object=agent_engine \
		--requirements-file=app/app_utils/.requirements.txt

# Alias for 'make deploy' for backward compatibility
backend: deploy


# ==============================================================================
# Infrastructure Setup
# ==============================================================================

# Set up development environment resources using Terraform
setup-dev-env:
	PROJECT_ID=$$(gcloud config get-value project) && \
	(cd deployment/terraform/dev && terraform init && terraform apply --var-file vars/env.tfvars --var dev_project_id=$$PROJECT_ID --auto-approve)

# ==============================================================================
# Testing & Code Quality
# ==============================================================================

# Run unit and integration tests
test:
	uv sync --dev
	uv run pytest tests/unit && uv run pytest tests/integration

# Run code quality checks (codespell, ruff, mypy)
lint:
	uv sync --dev --extra lint
	uv run codespell
	uv run ruff check . --diff
	uv run ruff format . --check --diff
	uv run mypy .

# ==============================================================================
# Docker Build & Deploy
# ==============================================================================

# Build Docker image
docker-build:
	docker build -t mapache-agent-army:latest .

# Build and push Docker image to Artifact Registry
docker-push: docker-build
	@PROJECT_ID=$$(gcloud config get-value project) && \
	REGION=us-central1 && \
	docker tag mapache-agent-army:latest $$REGION-docker.pkg.dev/$$PROJECT_ID/agents/mapache-agent-army:latest && \
	docker push $$REGION-docker.pkg.dev/$$PROJECT_ID/agents/mapache-agent-army:latest

# ==============================================================================
# Production Deployment
# ==============================================================================

# Deploy to staging environment
deploy-staging:
	@echo "Deploying to staging..."
	PROJECT_ID=$$(gcloud config get-value project) && \
	cd deployment/terraform && terraform apply -target=staging -auto-approve

# Deploy to production environment
deploy-prod:
	@echo "Deploying to production..."
	@echo "WARNING: This will deploy to PRODUCTION. Are you sure? (Press Ctrl+C to cancel)"
	@read -p "Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ] || exit 1
	PROJECT_ID=$$(gcloud config get-value project) && \
	cd deployment/terraform && terraform apply -target=production -auto-approve

# ==============================================================================
# Evaluation & Testing
# ==============================================================================

# Run Vertex AI evaluations
evaluate:
	@echo "Running agent evaluations..."
	uv run python -m evaluations.run_all

# Run load tests against staging
load-test-staging:
	@echo "Running load tests against staging..."
	uv run locust -f tests/load/locustfile.py --headless --users 10 --spawn-rate 1 --run-time 60s

# Run smoke tests against production
smoke-test-prod:
	@echo "Running smoke tests against production..."
	uv run pytest tests/smoke/ -v

# ==============================================================================
# Monitoring & Observability
# ==============================================================================

# View agent traces in Cloud Trace
view-traces:
	@PROJECT_ID=$$(gcloud config get-value project) && \
	echo "Opening Cloud Trace for project: $$PROJECT_ID" && \
	open "https://console.cloud.google.com/traces/list?project=$$PROJECT_ID"

# View agent logs in Cloud Logging
view-logs:
	@PROJECT_ID=$$(gcloud config get-value project) && \
	echo "Opening Cloud Logging for project: $$PROJECT_ID" && \
	open "https://console.cloud.google.com/logs?project=$$PROJECT_ID"

# View BigQuery analytics
view-analytics:
	@PROJECT_ID=$$(gcloud config get-value project) && \
	echo "Opening BigQuery for project: $$PROJECT_ID" && \
	open "https://console.cloud.google.com/bigquery?project=$$PROJECT_ID"

# ==============================================================================
# Cleanup
# ==============================================================================

# Clean build artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/

# ==============================================================================
# Gemini Enterprise Integration
# ==============================================================================

# Register the deployed agent to Gemini Enterprise
# Usage: ID="projects/.../engines/xxx" make register-gemini-enterprise
# Optional env vars: GEMINI_DISPLAY_NAME, GEMINI_DESCRIPTION, GEMINI_TOOL_DESCRIPTION, AGENT_ENGINE_ID
register-gemini-enterprise:
	uvx agent-starter-pack@0.20.4 register-gemini-enterprise

# ==============================================================================
# Help
# ==============================================================================

.PHONY: help
help:
	@echo "Mapache Agent Army - Available Commands"
	@echo ""
	@echo "Installation & Setup:"
	@echo "  make install              Install dependencies"
	@echo "  make setup-dev-env        Set up dev environment with Terraform"
	@echo ""
	@echo "Development:"
	@echo "  make playground           Launch local dev playground"
	@echo "  make test                 Run unit and integration tests"
	@echo "  make lint                 Run code quality checks"
	@echo "  make evaluate             Run Vertex AI evaluations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build         Build Docker image"
	@echo "  make docker-push          Build and push to Artifact Registry"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy               Deploy to Agent Engine (dev)"
	@echo "  make deploy-staging       Deploy to staging environment"
	@echo "  make deploy-prod          Deploy to production (with confirmation)"
	@echo ""
	@echo "Testing:"
	@echo "  make load-test-staging    Run load tests against staging"
	@echo "  make smoke-test-prod      Run smoke tests against production"
	@echo ""
	@echo "Monitoring:"
	@echo "  make view-traces          Open Cloud Trace console"
	@echo "  make view-logs            Open Cloud Logging console"
	@echo "  make view-analytics       Open BigQuery console"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean                Clean build artifacts"
	@echo ""

.DEFAULT_GOAL := help