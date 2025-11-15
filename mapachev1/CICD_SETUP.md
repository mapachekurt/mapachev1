# CI/CD Pipeline Setup Guide

Complete guide for setting up and using the multi-agent system CI/CD pipelines.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Pipeline Architecture](#pipeline-architecture)
4. [Setup Options](#setup-options)
5. [Configuration](#configuration)
6. [Deployment Workflow](#deployment-workflow)
7. [Monitoring and Operations](#monitoring-and-operations)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This project provides **two complete CI/CD pipeline options**:

### Option 1: GitHub Actions (Recommended)
- Native GitHub integration
- Workload Identity Federation (no service account keys)
- Rich UI with deployment tracking
- Free for public repos, included minutes for private repos

### Option 2: Cloud Build
- Native GCP integration
- Can trigger from GitHub, Bitbucket, or Cloud Source Repositories
- Advanced GCP features (scheduled builds, conditional triggers)
- Pay-as-you-go pricing

**Both options provide identical functionality:**
- ✅ Automated PR validation (lint, test, security scan)
- ✅ Staging deployment on merge to main
- ✅ Production deployment with manual approval
- ✅ Smoke tests and load testing
- ✅ Health monitoring and rollback procedures

---

## Quick Start

### Prerequisites

- ✅ Three GCP projects set up (CI/CD, Staging, Production)
- ✅ Terraform infrastructure deployed
- ✅ GitHub repository created
- ✅ Admin access to GitHub repository (for secrets/variables)

### For GitHub Actions (5 minutes)

```bash
# 1. Verify Terraform has created WIF resources
cd deployment/terraform
terraform output wif_provider_name

# 2. Get the values for GitHub secrets
terraform output -json | jq -r '{
  WIF_POOL_ID: .wif_provider_name.value | split("/")[5],
  WIF_PROVIDER_ID: .wif_provider_name.value | split("/")[7],
  GCP_SERVICE_ACCOUNT: .cicd_service_account_email.value
}'

# 3. Add secrets to GitHub
# Go to: Settings > Secrets and variables > Actions > New repository secret
# Add: WIF_POOL_ID, WIF_PROVIDER_ID, GCP_SERVICE_ACCOUNT

# 4. Add variables to GitHub
# Go to: Settings > Secrets and variables > Actions > Variables > New repository variable
# Add values from: terraform output -json

# 5. Set up production environment protection
# Go to: Settings > Environments > production > Add protection rules
# Check: Required reviewers, add your team

# 6. Done! Push code to trigger workflows
git push origin main
```

### For Cloud Build (10 minutes)

```bash
# 1. Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com \
  --project=YOUR_CICD_PROJECT_ID

# 2. Connect to GitHub
gcloud builds repositories create YOUR_REPO_NAME \
  --remote-uri=https://github.com/YOUR_ORG/YOUR_REPO.git \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1

# 3. Create triggers
gcloud builds triggers create github \
  --name="pr-validation" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --pull-request-pattern="^main$" \
  --build-config=.cloudbuild/pr.yaml \
  --project=YOUR_CICD_PROJECT_ID

gcloud builds triggers create github \
  --name="deploy-staging" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/staging.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --substitutions="_STAGING_PROJECT_ID=YOUR_STAGING_PROJECT"

gcloud builds triggers create github \
  --name="deploy-production" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/prod.yaml \
  --require-approval \
  --project=YOUR_CICD_PROJECT_ID \
  --substitutions="_STAGING_PROJECT_ID=YOUR_STAGING_PROJECT,_PROD_PROJECT_ID=YOUR_PROD_PROJECT"

# 4. Done! Merge a PR to trigger pipelines
```

---

## Pipeline Architecture

### Complete Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. DEVELOPMENT                                                  │
│    Developer creates PR → Pushes to feature branch             │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PR VALIDATION (Automatic)                                    │
│    ├── Lint (Ruff, mypy, codespell)                           │
│    ├── Unit Tests (pytest + coverage)                         │
│    ├── Integration Tests                                       │
│    ├── Security Scan (Safety, TruffleHog)                    │
│    └── Terraform Validation                                    │
│    Result: ✅ Pass → Allow merge  |  ❌ Fail → Block merge    │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. MERGE TO MAIN                                                │
│    PR approved → Merge to main → Delete feature branch         │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. STAGING DEPLOYMENT (Automatic)                               │
│    ├── Deploy to Staging Agent Engine                         │
│    ├── Run Smoke Tests                                        │
│    ├── Run Load Tests (Locust)                               │
│    ├── Health Check (error monitoring)                       │
│    └── Upload Results to GCS                                  │
│    Result: ✅ Ready for prod  |  ❌ Fix required              │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. PRODUCTION APPROVAL (Manual)                                 │
│    Team Lead reviews:                                           │
│    - Staging test results                                      │
│    - Error rates and monitoring                               │
│    - Manual testing results                                   │
│    Decision: ✅ Approve  |  ❌ Reject                          │
└────────────────────┬────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. PRODUCTION DEPLOYMENT (Manual Trigger)                       │
│    ├── Pre-flight Checks (validate staging)                   │
│    ├── Deploy to Production Agent Engine                      │
│    ├── Run Production Smoke Tests                            │
│    ├── Monitor for Errors (2 minutes)                        │
│    ├── Create Deployment Record                              │
│    └── Send Notifications                                     │
│    Result: ✅ Success  |  ❌ Rollback                         │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Files

| File | Purpose | Trigger | Duration |
|------|---------|---------|----------|
| `.github/workflows/pr.yaml` | PR validation | Pull request to main | ~5 min |
| `.github/workflows/deploy-staging.yaml` | Staging deployment | Merge to main | ~10 min |
| `.github/workflows/deploy-prod.yaml` | Production deployment | Manual only | ~10 min |
| `.cloudbuild/pr.yaml` | PR validation (Cloud Build) | Pull request to main | ~5 min |
| `.cloudbuild/staging.yaml` | Staging deployment (Cloud Build) | Merge to main | ~10 min |
| `.cloudbuild/prod.yaml` | Production deployment (Cloud Build) | Manual with approval | ~10 min |

---

## Setup Options

### GitHub Actions Setup (Detailed)

#### Step 1: Verify Terraform Outputs

```bash
cd deployment/terraform

# Check WIF configuration
terraform output wif_provider_name

# Get all CI/CD configuration
terraform output -json > /tmp/terraform-outputs.json
cat /tmp/terraform-outputs.json | jq
```

#### Step 2: Configure GitHub Secrets

Go to: `https://github.com/YOUR_ORG/YOUR_REPO/settings/secrets/actions`

Click **"New repository secret"** and add:

| Secret Name | Value Source |
|-------------|--------------|
| `WIF_POOL_ID` | From Terraform: `wif_provider_name` (extract pool ID) |
| `WIF_PROVIDER_ID` | From Terraform: `wif_provider_name` (extract provider ID) |
| `GCP_SERVICE_ACCOUNT` | From Terraform: `cicd_service_account_email` |

Extract values:
```bash
# WIF Pool ID
terraform output wif_provider_name | grep -oP 'workloadIdentityPools/\K[^/]+'

# WIF Provider ID
terraform output wif_provider_name | grep -oP 'providers/\K[^"]+'

# Service Account Email
terraform output cicd_service_account_email
```

#### Step 3: Configure GitHub Variables

Go to: `https://github.com/YOUR_ORG/YOUR_REPO/settings/variables/actions`

Click **"New repository variable"** and add:

| Variable Name | Value Source |
|---------------|--------------|
| `GCP_PROJECT_NUMBER` | From Terraform: `project_number` |
| `CICD_PROJECT_ID` | From Terraform: `cicd_project_id` |
| `STAGING_PROJECT_ID` | From Terraform: `staging_project_id` |
| `PROD_PROJECT_ID` | From Terraform: `prod_project_id` |
| `REGION` | From Terraform: `region` |
| `LOGS_BUCKET_NAME_STAGING` | From Terraform: `logs_buckets.staging` |
| `LOGS_BUCKET_NAME_PROD` | From Terraform: `logs_buckets.prod` |
| `ARTIFACT_REGISTRY_REPO_NAME` | From Terraform: `artifact_registry_repository` |
| `CONTAINER_NAME` | Your agent name (e.g., "mapachev1") |

Bulk add with script:
```bash
#!/bin/bash
# Save as: scripts/setup-github-vars.sh

ORG="YOUR_ORG"
REPO="YOUR_REPO"

# Extract values from Terraform
cd deployment/terraform
CICD_PROJECT=$(terraform output -raw cicd_project_id)
STAGING_PROJECT=$(terraform output -raw staging_project_id)
PROD_PROJECT=$(terraform output -raw prod_project_id)
REGION=$(terraform output -raw region)

# Set variables using gh CLI
gh variable set CICD_PROJECT_ID --body "$CICD_PROJECT" --repo "$ORG/$REPO"
gh variable set STAGING_PROJECT_ID --body "$STAGING_PROJECT" --repo "$ORG/$REPO"
gh variable set PROD_PROJECT_ID --body "$PROD_PROJECT" --repo "$ORG/$REPO"
gh variable set REGION --body "$REGION" --repo "$ORG/$REPO"
# ... add more
```

#### Step 4: Configure Environment Protection

1. Go to: `https://github.com/YOUR_ORG/YOUR_REPO/settings/environments`
2. Click on **"production"** environment
3. Under **"Deployment protection rules"**:
   - ✅ **Required reviewers**: Add team members who can approve
   - ⏱️ **Wait timer** (optional): 5-30 minutes minimum wait
   - 🔒 **Deployment branches**: Only `main` branch
4. Click **"Save protection rules"**

#### Step 5: Test the Setup

```bash
# Create test branch
git checkout -b test-cicd-setup

# Make a small change
echo "# CI/CD Test" >> README.md
git add README.md
git commit -m "test: CI/CD pipeline setup"

# Push and create PR
git push origin test-cicd-setup
gh pr create --title "Test CI/CD Setup" --body "Testing pipeline configuration"

# Watch the PR checks
gh pr checks --watch
```

### Cloud Build Setup (Detailed)

#### Step 1: Enable APIs

```bash
PROJECT_ID="YOUR_CICD_PROJECT_ID"

gcloud services enable cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  --project=$PROJECT_ID
```

#### Step 2: Configure Service Account Permissions

```bash
# Get Cloud Build service account
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant permissions in CI/CD project
for ROLE in roles/storage.admin roles/logging.logWriter roles/artifactregistry.writer; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${CB_SA}" \
    --role="$ROLE"
done

# Grant permissions in Staging project
STAGING_PROJECT="YOUR_STAGING_PROJECT_ID"
for ROLE in roles/aiplatform.user roles/iam.serviceAccountUser roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding $STAGING_PROJECT \
    --member="serviceAccount:${CB_SA}" \
    --role="$ROLE"
done

# Grant permissions in Production project
PROD_PROJECT="YOUR_PROD_PROJECT_ID"
for ROLE in roles/aiplatform.user roles/iam.serviceAccountUser roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding $PROD_PROJECT \
    --member="serviceAccount:${CB_SA}" \
    --role="$ROLE"
done
```

#### Step 3: Connect GitHub Repository

```bash
# Connect repository
gcloud builds repositories create YOUR_REPO_NAME \
  --remote-uri=https://github.com/YOUR_ORG/YOUR_REPO.git \
  --project=$PROJECT_ID \
  --region=us-central1

# Verify connection
gcloud builds repositories list --project=$PROJECT_ID --region=us-central1
```

#### Step 4: Create Build Triggers

```bash
# PR validation trigger
gcloud builds triggers create github \
  --name="pr-validation" \
  --description="Run tests and linting on pull requests" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --pull-request-pattern="^main$" \
  --comment-control=COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY \
  --build-config=.cloudbuild/pr.yaml \
  --project=$PROJECT_ID \
  --region=us-central1

# Staging deployment trigger
gcloud builds triggers create github \
  --name="deploy-staging" \
  --description="Deploy to staging on merge to main" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/staging.yaml \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --substitutions="_STAGING_PROJECT_ID=$STAGING_PROJECT,_REGION=us-central1,_LOGS_BUCKET_STAGING=${STAGING_PROJECT}-mapachev1-logs"

# Production deployment trigger (manual approval required)
gcloud builds triggers create github \
  --name="deploy-production" \
  --description="Deploy to production (requires approval)" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/prod.yaml \
  --require-approval \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --substitutions="_STAGING_PROJECT_ID=$STAGING_PROJECT,_PROD_PROJECT_ID=$PROD_PROJECT,_REGION=us-central1,_LOGS_BUCKET_STAGING=${STAGING_PROJECT}-mapachev1-logs,_LOGS_BUCKET_PROD=${PROD_PROJECT}-mapachev1-logs"
```

#### Step 5: Test Cloud Build

```bash
# Manual build submission for testing
gcloud builds submit \
  --config=.cloudbuild/pr.yaml \
  --project=$PROJECT_ID \
  --region=us-central1

# Watch build progress
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)') \
  --stream \
  --project=$PROJECT_ID
```

---

## Configuration

### Environment Variables

Both pipeline systems use these environment variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `PROJECT_ID` | Current GCP project | `my-staging-project` |
| `REGION` | GCP region | `us-central1` |
| `COMMIT_SHA` | Git commit hash | `abc123...` |
| `ENVIRONMENT` | Deployment target | `staging`, `production` |
| `AGENT_ENGINE_ID` | Deployed agent ID | `projects/.../reasoningEngines/123` |
| `ARTIFACTS_BUCKET_NAME` | GCS bucket for artifacts | `my-project-logs` |

### Customizing Test Suites

#### Add Custom Tests

```bash
# Create new test file
cat > tests/custom/test_business_logic.py << 'EOF'
import pytest

def test_custom_validation():
    # Your test logic
    assert True
EOF

# Update workflow to run custom tests
# In .github/workflows/pr.yaml, add:
- name: Run custom tests
  run: uv run pytest tests/custom/ -v
```

#### Modify Load Test Parameters

Edit `tests/load_test/load_test.py`:

```python
from locust import HttpUser, task, between

class AgentUser(HttpUser):
    wait_time = between(1, 5)  # Adjust wait time

    @task
    def query_agent(self):
        # Customize your load test
        pass
```

Update workflow parameters:
```yaml
# In deploy-staging.yaml
locust -f tests/load_test/load_test.py \
  --headless \
  -t 120s \     # Duration: 2 minutes
  -u 10 \       # Users: 10
  -r 2 \        # Spawn rate: 2/sec
```

---

## Deployment Workflow

### Day-to-Day Development

#### 1. Start New Feature

```bash
# Create feature branch
git checkout -b feature/awesome-new-capability
```

#### 2. Develop and Test Locally

```bash
# Make changes
vim app/agents/my_agent.py

# Run tests locally
uv run pytest tests/unit -v
uv run pytest tests/integration -v

# Lint code
uv run ruff check app/
uv run ruff format app/
uv run mypy app/
```

#### 3. Push and Create PR

```bash
# Commit and push
git add .
git commit -m "feat: add awesome new capability"
git push origin feature/awesome-new-capability

# Create PR
gh pr create --title "Add awesome new capability" --body "Description here"
```

#### 4. Wait for PR Checks

```bash
# Watch PR checks
gh pr checks --watch

# View detailed logs if something fails
gh run view --log
```

#### 5. Review and Merge

```bash
# After approval, merge
gh pr merge --squash --delete-branch
```

#### 6. Automatic Staging Deployment

Merging triggers automatic staging deployment. Monitor:

**GitHub Actions:**
```bash
gh run watch
```

**Cloud Build:**
```bash
gcloud builds list --ongoing --project=YOUR_CICD_PROJECT_ID
gcloud builds log BUILD_ID --stream
```

#### 7. Validate Staging

```bash
# Check deployment
gcloud ai reasoning-engines list \
  --project=YOUR_STAGING_PROJECT \
  --region=us-central1 \
  --limit=1

# View logs
gcloud logging read \
  "resource.type=\"aiplatform.googleapis.com/ReasoningEngine\"" \
  --project=YOUR_STAGING_PROJECT \
  --limit=50

# Check monitoring
open "https://console.cloud.google.com/monitoring?project=YOUR_STAGING_PROJECT"
```

#### 8. Deploy to Production

**GitHub Actions:**
```bash
# Trigger production deployment
gh workflow run deploy-prod.yaml

# Or via UI: Actions > Deploy to Production > Run workflow
```

**Cloud Build:**
```bash
# Trigger production build (will require approval)
gcloud builds triggers run deploy-production \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1 \
  --branch=main
```

#### 9. Approve Production Deployment

**GitHub Actions:**
- Go to Actions tab
- Click on the running workflow
- Click "Review deployments"
- Select "production" and click "Approve and deploy"

**Cloud Build:**
- Go to Cloud Build > Builds
- Find the pending build
- Click "Approve"

#### 10. Monitor Production

```bash
# Check deployment status
gcloud ai reasoning-engines describe AGENT_ENGINE_ID \
  --project=YOUR_PROD_PROJECT \
  --region=us-central1

# Monitor for errors
gcloud logging read \
  "resource.type=\"aiplatform.googleapis.com/ReasoningEngine\" AND severity>=ERROR" \
  --project=YOUR_PROD_PROJECT \
  --limit=100

# View metrics
open "https://console.cloud.google.com/monitoring/dashboards?project=YOUR_PROD_PROJECT"
```

### Emergency Rollback

If production deployment fails or causes issues:

#### GitHub Actions Rollback

```bash
# List recent deployments
gcloud ai reasoning-engines list \
  --project=YOUR_PROD_PROJECT \
  --region=us-central1 \
  --limit=5

# Trigger deployment with previous commit
gh workflow run deploy-prod.yaml \
  -f staging_commit_sha=PREVIOUS_WORKING_COMMIT

# Or revert the commit
git revert BAD_COMMIT_SHA
git push origin main
```

#### Cloud Build Rollback

```bash
# Find previous working build
gcloud builds list --limit=10 --project=YOUR_CICD_PROJECT_ID

# Re-run previous build
gcloud builds submit \
  --config=.cloudbuild/prod.yaml \
  --substitutions="COMMIT_SHA=PREVIOUS_COMMIT" \
  --project=YOUR_CICD_PROJECT_ID
```

---

## Monitoring and Operations

### View Build/Workflow Status

**GitHub Actions:**
```bash
# List recent runs
gh run list --limit=10

# View specific run
gh run view RUN_ID --log

# Download artifacts
gh run download RUN_ID
```

**Cloud Build:**
```bash
# List recent builds
gcloud builds list --limit=10

# View build details
gcloud builds describe BUILD_ID

# Stream logs
gcloud builds log BUILD_ID --stream
```

### Access Logs and Metrics

```bash
# Agent Engine logs
gcloud logging read \
  "resource.type=\"aiplatform.googleapis.com/ReasoningEngine\"" \
  --project=YOUR_PROJECT \
  --limit=100

# Load test results (in GCS)
gcloud storage ls gs://YOUR_PROJECT-mapachev1-logs/load-test-results/

# Download load test report
gcloud storage cp gs://YOUR_PROJECT-mapachev1-logs/load-test-results/TIMESTAMP/report.html .
```

### Monitoring Dashboards

- **Cloud Monitoring**: https://console.cloud.google.com/monitoring
- **Cloud Logging**: https://console.cloud.google.com/logs
- **Cloud Trace**: https://console.cloud.google.com/traces
- **Agent Engine**: https://console.cloud.google.com/vertex-ai/agent-builder/engines

### Notifications

#### Slack Integration

1. Create Slack incoming webhook
2. Add to GitHub variables (GitHub Actions) or Secret Manager (Cloud Build)
3. Set `SLACK_WEBHOOK_URL` variable
4. Workflows will automatically send notifications

---

## Troubleshooting

### Common Issues

#### 1. Authentication Fails

**Error:** `Error authenticating with Google Cloud`

**GitHub Actions Fix:**
```bash
# Verify WIF setup
gcloud iam workload-identity-pools describe github-pool \
  --project=YOUR_CICD_PROJECT \
  --location=global

# Check bindings
gcloud iam service-accounts get-iam-policy YOUR_SA_EMAIL
```

**Cloud Build Fix:**
```bash
# Check service account permissions
gcloud projects get-iam-policy YOUR_PROJECT \
  --flatten="bindings[].members" \
  --filter="bindings.members:*@cloudbuild.gserviceaccount.com"
```

#### 2. Tests Fail in CI but Pass Locally

**Checklist:**
- [ ] Python version matches (3.12)
- [ ] Dependencies locked with `uv.lock`
- [ ] Environment variables set
- [ ] GCP permissions granted
- [ ] Test data available

**Debug:**
```yaml
# Add to workflow
- name: Debug
  run: |
    python --version
    pip list
    env | sort
```

#### 3. Deployment Timeouts

**Fix:** Increase timeout in workflow:

```yaml
# GitHub Actions
timeout-minutes: 30

# Cloud Build
timeout: 1800s
```

#### 4. Production Approval Not Working

**GitHub Actions:**
- Verify environment protection configured
- Check required reviewers added
- Ensure reviewer has appropriate permissions

**Cloud Build:**
- Verify trigger has `--require-approval` flag
- Check IAM permissions for approvers

#### 5. Load Tests Fail

**Checklist:**
- [ ] Locust installed
- [ ] Test file exists: `tests/load_test/load_test.py`
- [ ] Auth token valid
- [ ] Agent Engine accessible

**Debug:**
```bash
# Test locally
export _AUTH_TOKEN=$(gcloud auth print-access-token)
export PROJECT_ID=your-project
export REGION=us-central1

pip install locust
locust -f tests/load_test/load_test.py --headless -t 10s -u 1
```

### Getting Help

1. **Check logs**: GitHub Actions UI or Cloud Build console
2. **Review documentation**: This file and workflow READMEs
3. **Search issues**: GitHub repository issues
4. **Contact team**: DevOps or platform team

### Useful Commands

```bash
# GitHub CLI
gh auth login              # Authenticate
gh repo view              # View repository
gh pr list                # List PRs
gh workflow list          # List workflows
gh run list               # List workflow runs

# gcloud CLI
gcloud auth login                    # Authenticate
gcloud config set project PROJECT_ID  # Set project
gcloud builds list                   # List builds
gcloud ai reasoning-engines list     # List agents
gcloud logging read                  # Read logs
```

---

## Additional Resources

- [GitHub Actions Documentation](.github/workflows/README.md)
- [Cloud Build Documentation](.cloudbuild/README.md)
- [Terraform Infrastructure](deployment/terraform/)
- [Agent Starter Pack Best Practices](docs/analysis/06_best_practices_summary.md)
- [Deployment Patterns](docs/analysis/03_deploy_patterns.md)

---

**Questions or Issues?** Contact the DevOps team or create an issue in the repository.
