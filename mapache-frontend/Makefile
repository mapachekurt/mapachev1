# Mapache Frontend Makefile
# Simplify common development and deployment tasks

.PHONY: help install dev build test lint clean docker-build docker-run deploy deploy-manual setup-gcp

# Default target
help:
	@echo "Mapache Frontend - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "Development:"
	@echo "  make install          - Install dependencies"
	@echo "  make dev              - Start development server"
	@echo "  make build            - Build for production"
	@echo "  make start            - Start production server"
	@echo "  make test             - Run tests"
	@echo "  make test-e2e         - Run E2E tests"
	@echo "  make lint             - Run linter"
	@echo "  make clean            - Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container locally"
	@echo "  make docker-push      - Push Docker image to GCR"
	@echo ""
	@echo "Deployment (GCP):"
	@echo "  make setup-gcp        - Configure GCP project and enable APIs"
	@echo "  make deploy           - Deploy to Cloud Run (quick)"
	@echo "  make deploy-manual    - Build and deploy manually"
	@echo "  make deploy-prod      - Deploy to production with optimizations"
	@echo "  make logs             - View Cloud Run logs"
	@echo "  make status           - Check deployment status"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	npm install

# Development
dev:
	@echo "Starting development server..."
	npm run dev

build:
	@echo "Building for production..."
	npm run build

start:
	@echo "Starting production server..."
	npm start

# Testing
test:
	@echo "Running tests..."
	npm test

test-e2e:
	@echo "Running E2E tests..."
	npm run test:e2e

lint:
	@echo "Running linter..."
	npm run lint

# Clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf .next
	rm -rf node_modules
	rm -rf dist
	rm -rf coverage

# Docker commands
docker-build:
	@echo "Building Docker image..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	docker build -t gcr.io/$(PROJECT_ID)/mapache-frontend:latest .

docker-run:
	@echo "Running Docker container locally..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	docker run -p 3000:3000 \
		-e NEXT_PUBLIC_API_URL=${BACKEND_URL:-http://localhost:8080} \
		-e NEXT_PUBLIC_WS_URL=${WS_URL:-ws://localhost:8080/ws} \
		gcr.io/$(PROJECT_ID)/mapache-frontend:latest

docker-push:
	@echo "Pushing Docker image to GCR..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	gcloud auth configure-docker
	docker push gcr.io/$(PROJECT_ID)/mapache-frontend:latest

# GCP Setup
setup-gcp:
	@echo "Setting up GCP project..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	gcloud config set project $(PROJECT_ID)
	@echo "Enabling required APIs..."
	gcloud services enable cloudbuild.googleapis.com
	gcloud services enable run.googleapis.com
	gcloud services enable containerregistry.googleapis.com
	gcloud services enable secretmanager.googleapis.com
	@echo "GCP setup complete!"

# Deployment
deploy:
	@echo "Deploying to Cloud Run (quick deploy)..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	gcloud run deploy mapache-frontend \
		--source . \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
		--set-env-vars="NEXT_PUBLIC_WS_URL=${WS_URL}" \
		--set-env-vars="NEXT_TELEMETRY_DISABLED=1"

deploy-manual: docker-build docker-push
	@echo "Deploying to Cloud Run (manual)..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	gcloud run deploy mapache-frontend \
		--image gcr.io/$(PROJECT_ID)/mapache-frontend:latest \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--port 3000

deploy-prod:
	@echo "Deploying to production with optimizations..."
	@if [ -z "$(PROJECT_ID)" ]; then \
		echo "Error: PROJECT_ID not set. Run: export PROJECT_ID=your-project-id"; \
		exit 1; \
	fi
	gcloud run deploy mapache-frontend \
		--source . \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--port 3000 \
		--memory 512Mi \
		--cpu 1 \
		--min-instances 1 \
		--max-instances 50 \
		--concurrency 80 \
		--timeout 300 \
		--set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
		--set-env-vars="NEXT_PUBLIC_WS_URL=${WS_URL}" \
		--set-env-vars="NEXT_TELEMETRY_DISABLED=1"

# Monitoring
logs:
	@echo "Fetching Cloud Run logs..."
	gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend"

logs-errors:
	@echo "Fetching error logs..."
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend AND severity>=ERROR" \
		--limit 50

status:
	@echo "Checking deployment status..."
	gcloud run services describe mapache-frontend \
		--region us-central1 \
		--format="table(status.url,status.latestReadyRevisionName,status.conditions[0].type)"

# Utilities
url:
	@echo "Getting service URL..."
	@gcloud run services describe mapache-frontend \
		--region us-central1 \
		--format="value(status.url)"

health:
	@echo "Checking service health..."
	@SERVICE_URL=$$(gcloud run services describe mapache-frontend --region us-central1 --format="value(status.url)"); \
	curl -I $$SERVICE_URL
