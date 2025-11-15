# Multi-Agent System Deployment Guide

This directory contains the complete infrastructure-as-code configuration for deploying the MapacheV1 multi-agent system to Google Cloud Platform, following Agent Starter Pack best practices.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Detailed Setup](#detailed-setup)
6. [Deploying to Environments](#deploying-to-environments)
7. [Terraform Resources](#terraform-resources)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Overview

This Terraform configuration provisions a production-ready, multi-environment infrastructure for AI agent systems with:

- **Multi-Environment Support**: Separate staging and production environments
- **CI/CD Integration**: Automated deployments via GitHub Actions or Cloud Build
- **Observability**: BigQuery log sinks, Cloud Trace, and monitoring dashboards
- **Security**: Least-privilege IAM, Workload Identity Federation, no service account keys
- **Cost Optimization**: Lifecycle policies, appropriate instance scaling
- **Scalability**: Artifact Registry, Cloud Run, auto-scaling configurations

### Infrastructure Components

| Resource Type | Purpose | Count |
|--------------|---------|-------|
| GCP Projects | Staging, Production, CI/CD | 3 |
| Service Accounts | App runtime, CI/CD, pipelines | 5 |
| Storage Buckets | Logs, traces, data ingestion | 9 |
| BigQuery Datasets | Telemetry, feedback, analytics, evaluations | 8 |
| Artifact Registry | Docker images | 1 |
| Alert Policies | Error rate, latency, cost | 6+ |
| Dashboards | Agent performance metrics | 2 |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CI/CD Project                              │
│                                                                 │
│  ┌──────────────────┐      ┌─────────────────────┐            │
│  │ GitHub Actions/  │─────▶│ Artifact Registry   │            │
│  │ Cloud Build      │      │ (Docker Images)     │            │
│  └──────────────────┘      └─────────────────────┘            │
│           │                                                     │
│           │ Deploy                                             │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ├────────────────────┬────────────────────┐
            ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Dev Environment  │  │Staging Environment│  │ Prod Environment │
│                  │  │                   │  │                  │
│ • Cloud Run      │  │ • Cloud Run       │  │ • Cloud Run      │
│ • App SA         │  │ • App SA          │  │ • App SA         │
│ • BigQuery       │  │ • BigQuery        │  │ • BigQuery       │
│ • GCS Buckets    │  │ • GCS Buckets     │  │ • GCS Buckets    │
│ • Monitoring     │  │ • Monitoring      │  │ • Monitoring     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### Data Flow

```
User Request → Cloud Run → Agent → Vertex AI (Gemini)
                  │           │
                  ▼           ▼
            Cloud Logging  Cloud Trace
                  │           │
                  ▼           ▼
            BigQuery      GCS (>256KB spans)
                  │
                  ▼
          Analytics Views
```

---

## Prerequisites

### Required Tools

1. **Terraform** >= 1.0.0
   ```bash
   # Install via Homebrew (Mac)
   brew install terraform

   # Or download from https://www.terraform.io/downloads
   terraform --version
   ```

2. **Google Cloud SDK** (gcloud CLI)
   ```bash
   # Install
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL

   # Initialize and authenticate
   gcloud init
   gcloud auth application-default login
   ```

3. **GitHub CLI** (for GitHub Actions setup)
   ```bash
   brew install gh
   gh auth login
   ```

### GCP Setup

1. **Three GCP Projects** (or one for dev):
   - CI/CD project (hosts Cloud Build/Artifact Registry)
   - Staging project
   - Production project

2. **Billing Enabled** on all projects

3. **Required APIs** (will be enabled by Terraform):
   - Cloud Resource Manager API
   - Service Usage API
   - IAM API
   - Cloud Build API (if using Cloud Build)
   - Artifact Registry API
   - Cloud Run API
   - Vertex AI API
   - BigQuery API
   - Cloud Logging API
   - Cloud Monitoring API
   - Cloud Trace API

4. **IAM Permissions** - Your user account needs:
   - `roles/owner` or
   - `roles/editor` + `roles/iam.securityAdmin` + `roles/resourcemanager.projectIamAdmin`

### GitHub Setup (for GitHub Actions)

1. **GitHub Repository** created
2. **Repository Access** for creating secrets (admin or write)

---

## Quick Start

For users who want to get started quickly:

```bash
# 1. Navigate to terraform directory
cd deployment/terraform

# 2. Copy example variables
cp terraform.tfvars.example terraform.tfvars

# 3. Edit terraform.tfvars with your project IDs
nano terraform.tfvars

# 4. Initialize Terraform
terraform init

# 5. Review planned changes
terraform plan

# 6. Apply configuration
terraform apply

# 7. View outputs
terraform output
```

That's it! Your infrastructure is deployed.

---

## Detailed Setup

### Step 1: Configure Terraform Backend

The backend is already configured to use GCS for remote state:

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "YOUR_TERRAFORM_STATE_BUCKET"
    prefix = "terraform/state"
  }
}
```

Create the state bucket:

```bash
# Replace with your CI/CD project ID
export PROJECT_ID="my-cicd-project"

# Create bucket for Terraform state
gsutil mb -p ${PROJECT_ID} -l us-central1 gs://${PROJECT_ID}-terraform-state

# Enable versioning (important for rollback)
gsutil versioning set on gs://${PROJECT_ID}-terraform-state

# Update backend.tf with your bucket name
sed -i '' "s/YOUR_TERRAFORM_STATE_BUCKET/${PROJECT_ID}-terraform-state/g" backend.tf
```

### Step 2: Configure Variables

Copy and edit the example variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
# Core configuration
project_name           = "mapachev1"
region                = "us-central1"

# Project IDs
cicd_runner_project_id = "my-org-cicd-12345"
staging_project_id     = "my-org-staging-67890"
prod_project_id        = "my-org-prod-11111"

# GitHub
repository_owner = "my-github-org"
repository_name  = "mapachev1"

# Monitoring
alert_email   = "ops-team@example.com"
enable_alerts = true
```

### Step 3: Initialize Terraform

```bash
# Initialize providers and backend
terraform init

# Validate configuration
terraform validate

# Format configuration files
terraform fmt -recursive
```

### Step 4: Plan Infrastructure Changes

```bash
# Generate and review execution plan
terraform plan -out=tfplan

# Optional: Save plan to file for review
terraform show -json tfplan > plan.json
```

### Step 5: Apply Infrastructure

```bash
# Apply the plan
terraform apply tfplan

# Or apply directly (will prompt for confirmation)
terraform apply

# For auto-approval (use with caution)
terraform apply -auto-approve
```

**Expected Duration**: 5-10 minutes

### Step 6: Verify Deployment

```bash
# View all outputs
terraform output

# View specific output
terraform output deployment_summary

# Test service account creation
gcloud iam service-accounts list --project=YOUR_PROJECT_ID

# Verify BigQuery datasets
bq ls --project_id=YOUR_PROJECT_ID

# Check Artifact Registry
gcloud artifacts repositories list --project=YOUR_CICD_PROJECT_ID
```

---

## Deploying to Environments

### Development Environment

For local development and testing:

```bash
cd deployment/terraform/dev

# Configure dev-specific variables
cp vars/env.tfvars.example vars/env.tfvars
nano vars/env.tfvars

# Deploy dev infrastructure
terraform init
terraform plan -var-file=vars/env.tfvars
terraform apply -var-file=vars/env.tfvars
```

### Staging Environment

Staging is automatically deployed when you merge to `main` branch (via GitHub Actions).

**Manual deployment:**

```bash
# Build and push Docker image
export REGION="us-central1"
export CICD_PROJECT="my-cicd-project"
export STAGING_PROJECT="my-staging-project"
export IMAGE_TAG="$(git rev-parse --short HEAD)"

# Build image
docker build -t ${REGION}-docker.pkg.dev/${CICD_PROJECT}/mapachev1-docker/agent:${IMAGE_TAG} .

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Push image
docker push ${REGION}-docker.pkg.dev/${CICD_PROJECT}/mapachev1-docker/agent:${IMAGE_TAG}

# Deploy to Cloud Run
gcloud run deploy mapachev1 \
  --image ${REGION}-docker.pkg.dev/${CICD_PROJECT}/mapachev1-docker/agent:${IMAGE_TAG} \
  --project ${STAGING_PROJECT} \
  --region ${REGION} \
  --service-account mapachev1-app@${STAGING_PROJECT}.iam.gserviceaccount.com \
  --platform managed \
  --allow-unauthenticated
```

### Production Environment

Production deployments require manual approval (GitHub Actions environment protection).

**GitHub Actions workflow:**

1. Merge PR to `main` → Staging deployment
2. Staging tests pass
3. Create release tag: `git tag v1.0.0 && git push origin v1.0.0`
4. Production workflow triggers
5. **Manual approval required**
6. Same Docker image promoted from staging to prod

**Manual production deployment:**

```bash
# Get image from staging
export STAGING_IMAGE=$(gcloud run services describe mapachev1 \
  --project=${STAGING_PROJECT} \
  --region=${REGION} \
  --format='value(spec.template.spec.containers[0].image)')

# Deploy to production
export PROD_PROJECT="my-prod-project"

gcloud run deploy mapachev1 \
  --image ${STAGING_IMAGE} \
  --project ${PROD_PROJECT} \
  --region ${REGION} \
  --service-account mapachev1-app@${PROD_PROJECT}.iam.gserviceaccount.com \
  --platform managed \
  --no-traffic  # Deploy without routing traffic

# Verify deployment
gcloud run revisions list \
  --service mapachev1 \
  --project ${PROD_PROJECT} \
  --region ${REGION}

# Gradually shift traffic
gcloud run services update-traffic mapachev1 \
  --to-revisions LATEST=10 \
  --project ${PROD_PROJECT} \
  --region ${REGION}

# Monitor for 5-10 minutes, then full rollout
gcloud run services update-traffic mapachev1 \
  --to-revisions LATEST=100 \
  --project ${PROD_PROJECT} \
  --region ${REGION}
```

---

## Terraform Resources

### File Structure

```
deployment/terraform/
├── providers.tf              # Provider configuration
├── variables.tf              # Input variable definitions
├── locals.tf                 # Computed local values
├── service_accounts.tf       # Service account creation
├── iam.tf                    # IAM role bindings
├── apis.tf                   # GCP API enablement
├── storage.tf                # GCS buckets, Artifact Registry
├── log_sinks.tf              # BigQuery log routing
├── bigquery.tf               # Analytics datasets and views
├── monitoring.tf             # Alert policies and dashboards
├── outputs.tf                # Output values for CI/CD
├── backend.tf                # Remote state configuration
├── github.tf                 # GitHub Actions integration
├── wif.tf                    # Workload Identity Federation
├── terraform.tfvars.example  # Example configuration
└── dev/                      # Dev environment overrides
    ├── providers.tf
    ├── variables.tf
    ├── iam.tf
    ├── apis.tf
    ├── storage.tf
    ├── log_sinks.tf
    └── vars/
        └── env.tfvars
```

### Key Resources

#### Service Accounts

| Service Account | Purpose | Roles |
|----------------|---------|-------|
| `mapachev1-cb` | CI/CD runner | Cloud Build, Artifact Registry writer |
| `mapachev1-app` (staging) | Agent runtime | Vertex AI user, logging, tracing |
| `mapachev1-app` (prod) | Agent runtime | Vertex AI user, logging, tracing |

#### Storage Buckets

| Bucket | Purpose | Lifecycle |
|--------|---------|-----------|
| `*-logs` | Build and application logs | 30 days |
| `*-trace-payloads` | Large trace spans (>256KB) | 7 days |
| `*-data-ingestion` | RAG data pipeline | Indefinite (versioned) |

#### BigQuery Datasets

| Dataset | Purpose | Tables/Views |
|---------|---------|--------------|
| `mapachev1_telemetry` | Raw telemetry logs | Partitioned by day |
| `mapachev1_feedback` | User feedback | Partitioned by day |
| `mapachev1_analytics` | Performance metrics | `agent_performance`, `cost_analysis` views |
| `mapachev1_evaluations` | Vertex AI evaluations | Evaluation results |

---

## Monitoring and Observability

### Cloud Monitoring Dashboards

Access dashboards via Terraform outputs:

```bash
terraform output console_urls
```

Or navigate directly:
- **Staging**: `https://console.cloud.google.com/monitoring/dashboards/custom/{dashboard-id}?project={staging-project-id}`
- **Production**: `https://console.cloud.google.com/monitoring/dashboards/custom/{dashboard-id}?project={prod-project-id}`

### Alert Policies

Configured alerts (if `enable_alerts = true`):

1. **High Error Rate**: Triggers when 5xx errors > 5% for 5 minutes
2. **High P99 Latency**: Triggers when P99 latency > 10 seconds
3. **High Daily Cost**: Triggers when daily LLM costs > $100 (production only)
4. **Low Request Rate**: Triggers when requests drop significantly (production only)
5. **Instance Scaling**: Triggers when Cloud Run instances maxed out
6. **Uptime Check**: HTTP health check failures (production only)

### BigQuery Analytics

Query agent performance:

```sql
-- Agent performance by hour
SELECT *
FROM `{project-id}.mapachev1_analytics.agent_performance`
WHERE hour >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
ORDER BY hour DESC, invocation_count DESC;
```

Query cost analysis:

```sql
-- Daily cost breakdown
SELECT *
FROM `{project-id}.mapachev1_analytics.cost_analysis`
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
ORDER BY date DESC, estimated_cost_usd DESC;
```

### Cloud Trace

View distributed traces:

```bash
# Get trace URL from outputs
terraform output console_urls | jq '.prod.traces'

# Or construct manually
open "https://console.cloud.google.com/traces/list?project={prod-project-id}"
```

### Cloud Logging

Query logs:

```bash
# Recent errors
gcloud logging read \
  "resource.type=cloud_run_revision \
   AND severity>=ERROR \
   AND resource.labels.service_name=mapachev1" \
  --limit=50 \
  --project={project-id} \
  --format=json

# Telemetry logs
gcloud logging read \
  "labels.type=\"agent_telemetry\"" \
  --limit=100 \
  --project={project-id}
```

---

## Troubleshooting

### Common Issues

#### 1. Terraform Init Fails

**Error**: `Backend configuration changed`

**Solution**:
```bash
terraform init -reconfigure
```

#### 2. Insufficient Permissions

**Error**: `Error creating Project: googleapi: Error 403: User is not authorized`

**Solution**:
```bash
# Grant yourself necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member=user:YOUR_EMAIL \
  --role=roles/owner
```

#### 3. API Not Enabled

**Error**: `Error 403: {API} API has not been used in project {project-id}`

**Solution**: Terraform should auto-enable APIs, but you can manually enable:
```bash
gcloud services enable SERVICE_NAME.googleapis.com --project=PROJECT_ID
```

#### 4. Resource Already Exists

**Error**: `Error: A resource with this name already exists`

**Solution**: Import existing resource:
```bash
terraform import google_storage_bucket.logs_data_bucket[\"project-id\"] project-id/bucket-name
```

#### 5. Docker Push Permission Denied

**Error**: `denied: Permission "artifactregistry.repositories.uploadArtifacts" denied`

**Solution**:
```bash
# Re-authenticate Docker
gcloud auth configure-docker us-central1-docker.pkg.dev

# Verify IAM permissions
gcloud artifacts repositories get-iam-policy REPO_NAME \
  --project=PROJECT_ID \
  --location=REGION
```

### Debug Commands

```bash
# Check Terraform state
terraform show

# List all resources
terraform state list

# Inspect specific resource
terraform state show 'google_service_account.app_sa["prod"]'

# Enable debug logging
export TF_LOG=DEBUG
terraform plan
```

### Rollback Procedures

#### Rollback Terraform Changes

```bash
# View state versions
gsutil ls -l gs://YOUR_STATE_BUCKET/terraform/state/

# Restore previous version
gsutil cp gs://YOUR_STATE_BUCKET/terraform/state/default.tfstate#{VERSION} \
  gs://YOUR_STATE_BUCKET/terraform/state/default.tfstate

# Re-initialize
terraform init
```

#### Rollback Cloud Run Deployment

```bash
# List revisions
gcloud run revisions list --service=mapachev1 --project=PROJECT_ID

# Rollback to previous revision
gcloud run services update-traffic mapachev1 \
  --to-revisions PREVIOUS_REVISION=100 \
  --project=PROJECT_ID \
  --region=REGION
```

---

## Best Practices

### 1. State Management

- **Always use remote state** (GCS backend)
- **Enable versioning** on state bucket
- **Use state locking** (automatic with GCS)
- **Never commit state files** to Git

### 2. Secret Management

- **Never commit secrets** to Git
- **Use Secret Manager** for sensitive values
- **Rotate secrets regularly** (90 days)
- **Use WIF instead of service account keys**

### 3. IAM and Security

- **Least privilege**: Grant minimum required permissions
- **Separate service accounts**: Different SAs for CI/CD and runtime
- **Audit IAM changes**: Review IAM bindings quarterly
- **No long-lived credentials**: Use WIF for CI/CD

### 4. Cost Optimization

- **Set lifecycle policies** on storage buckets
- **Monitor costs daily**: Review BigQuery cost analysis view
- **Use appropriate instance sizes**: Don't over-provision Cloud Run
- **Clean up unused resources**: Run periodic audits

### 5. Deployment Workflow

- **Always deploy to staging first**
- **Run smoke tests** before production promotion
- **Use canary deployments** for production (gradual rollout)
- **Have rollback plan** ready before deploying

### 6. Monitoring

- **Set up alerts early**: Don't wait for production issues
- **Review dashboards weekly**: Identify trends and anomalies
- **Test alert policies**: Manually trigger to verify notifications
- **Document runbooks**: Create playbooks for common alerts

### 7. Infrastructure as Code

- **Format code**: Run `terraform fmt` before commits
- **Validate changes**: Always run `terraform plan` before `apply`
- **Use modules**: Extract reusable components
- **Document changes**: Add comments for complex logic

---

## Next Steps

After deploying infrastructure:

1. **Configure CI/CD Pipeline**
   - Set up GitHub Actions secrets (from `terraform output`)
   - Test CI/CD workflow with sample deployment
   - Configure branch protection rules

2. **Deploy Your Agent**
   - Build Docker image
   - Push to Artifact Registry
   - Deploy to staging
   - Run integration tests

3. **Set Up Monitoring**
   - Configure alert notification channels
   - Create custom dashboards
   - Set up on-call rotation

4. **Production Readiness**
   - Load testing in staging
   - Security review
   - Documentation review
   - Runbook creation

5. **Ongoing Operations**
   - Weekly metric reviews
   - Monthly cost optimization
   - Quarterly security audits
   - Regular dependency updates

---

## Additional Resources

- [Agent Starter Pack Documentation](https://googlecloudplatform.github.io/agent-starter-pack/)
- [Terraform Google Provider Docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Cloud Monitoring Best Practices](https://cloud.google.com/monitoring/best-practices)

---

## Support

For issues and questions:

- **GitHub Issues**: [Create an issue](https://github.com/your-org/mapachev1/issues)
- **Team Slack**: #mapachev1-ops
- **Documentation**: `docs/` directory in this repository

---

**Last Updated**: 2025-11-15
**Maintainer**: Platform Engineering Team
**Terraform Version**: >= 1.0.0
**Google Provider Version**: ~> 7.10.0
