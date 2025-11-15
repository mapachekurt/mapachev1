# Cloud Build CI/CD Pipelines

This directory contains Cloud Build configurations for the multi-agent system deployment pipeline.

## Overview

These Cloud Build configurations provide an alternative to GitHub Actions for CI/CD. They integrate directly with Google Cloud Platform and can be triggered from GitHub, Bitbucket, or Google Cloud Source Repositories.

## Pipeline Files

### 1. `pr.yaml` - Pull Request Validation

**Triggers:** Pull requests to `main` branch

**Steps:**
- Install dependencies with uv
- Run Ruff linter and formatter
- Run mypy type checking
- Run codespell for spell checking
- Execute unit tests with coverage
- Execute integration tests
- Security scanning with Safety
- Terraform validation

**Timeout:** 30 minutes

**Usage:**
```bash
# Manual trigger for testing
gcloud builds submit --config=.cloudbuild/pr.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --substitutions=_REGION=us-central1,_PROJECT_NAME=mapachev1
```

### 2. `staging.yaml` - Staging Deployment

**Triggers:** Merge to `main` branch

**Steps:**
1. Install dependencies
2. Pre-deployment validation tests
3. Export requirements for Agent Engine
4. Deploy to Staging Agent Engine
5. Verify deployment
6. Run smoke tests
7. Run load tests with Locust
8. Upload results to GCS
9. Health check and error monitoring
10. Deployment summary

**Outputs:**
- Agent Engine ID saved to GCS
- Load test results uploaded to logs bucket
- Deployment artifacts preserved

**Timeout:** 30 minutes

**Usage:**
```bash
# Manual staging deployment
gcloud builds submit --config=.cloudbuild/staging.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --substitutions=_STAGING_PROJECT_ID=your-staging-project,_REGION=us-central1
```

### 3. `prod.yaml` - Production Deployment

**Triggers:** Manual approval required (configure in Cloud Build trigger)

**Steps:**
1. Pre-deployment validation checks
2. Verify staging deployment exists
3. Check error rates in staging
4. Install dependencies and export requirements
5. Create deployment audit record
6. Deploy to Production Agent Engine
7. Verify production deployment
8. Run production smoke tests
9. Monitor for immediate errors (2 minutes)
10. Update deployment record
11. Generate deployment summary

**Safety Features:**
- Pre-flight checks for staging health
- Smoke tests before marking success
- Error monitoring in first 2 minutes
- Deployment audit trail in GCS
- Rollback instructions on failure

**Timeout:** 30 minutes

**Usage:**
```bash
# Manual production deployment (requires approval)
gcloud builds submit --config=.cloudbuild/prod.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --substitutions=_STAGING_PROJECT_ID=staging-project,_PROD_PROJECT_ID=prod-project,_REGION=us-central1
```

## Setup Instructions

### 1. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com \
  --project=YOUR_CICD_PROJECT_ID

gcloud services enable secretmanager.googleapis.com \
  --project=YOUR_CICD_PROJECT_ID
```

### 2. Configure Cloud Build Service Account

The Cloud Build service account needs permissions in all three projects (CICD, Staging, Production):

```bash
# Get the Cloud Build service account email
PROJECT_NUMBER=$(gcloud projects describe YOUR_CICD_PROJECT_ID --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

# Grant roles in CICD project
gcloud projects add-iam-policy-binding YOUR_CICD_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_CICD_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/logging.logWriter"

# Grant roles in Staging project
gcloud projects add-iam-policy-binding YOUR_STAGING_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_STAGING_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/iam.serviceAccountUser"

# Grant roles in Production project
gcloud projects add-iam-policy-binding YOUR_PROD_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROD_PROJECT_ID \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/iam.serviceAccountUser"
```

### 3. Create Cloud Build Triggers

#### PR Validation Trigger

```bash
gcloud builds triggers create github \
  --name="pr-validation" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --pull-request-pattern="^main$" \
  --build-config=.cloudbuild/pr.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1
```

#### Staging Deployment Trigger

```bash
gcloud builds triggers create github \
  --name="deploy-staging" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/staging.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1 \
  --substitutions="_STAGING_PROJECT_ID=your-staging-project,_REGION=us-central1,_LOGS_BUCKET_STAGING=your-staging-project-mapachev1-logs"
```

#### Production Deployment Trigger (Manual)

```bash
gcloud builds triggers create github \
  --name="deploy-production" \
  --repo-name=YOUR_REPO_NAME \
  --repo-owner=YOUR_GITHUB_ORG \
  --branch-pattern="^main$" \
  --build-config=.cloudbuild/prod.yaml \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1 \
  --require-approval \
  --substitutions="_STAGING_PROJECT_ID=your-staging-project,_PROD_PROJECT_ID=your-prod-project,_REGION=us-central1,_LOGS_BUCKET_STAGING=staging-logs,_LOGS_BUCKET_PROD=prod-logs"
```

### 4. Connect to GitHub

You need to connect Cloud Build to your GitHub repository:

```bash
# This will open a browser for GitHub OAuth
gcloud builds repositories create YOUR_REPO_NAME \
  --remote-uri=https://github.com/YOUR_ORG/YOUR_REPO.git \
  --connection=YOUR_CONNECTION_NAME \
  --project=YOUR_CICD_PROJECT_ID \
  --region=us-central1
```

Or use the Cloud Console:
1. Go to Cloud Build > Triggers
2. Click "Connect Repository"
3. Select "GitHub" and authorize
4. Select your repository

## Monitoring and Logs

### View Build History

```bash
# List recent builds
gcloud builds list --project=YOUR_CICD_PROJECT_ID --limit=10

# View specific build details
gcloud builds describe BUILD_ID --project=YOUR_CICD_PROJECT_ID

# Stream build logs
gcloud builds log BUILD_ID --project=YOUR_CICD_PROJECT_ID --stream
```

### Access Build Logs in GCS

Build logs are automatically uploaded to the configured logs bucket:

```bash
# List logs
gcloud storage ls gs://YOUR_PROJECT_ID-mapachev1-logs/

# Download build logs
gcloud storage cp gs://YOUR_PROJECT_ID-mapachev1-logs/log-BUILD_ID.txt .
```

### View in Cloud Console

- Build History: https://console.cloud.google.com/cloud-build/builds
- Build Triggers: https://console.cloud.google.com/cloud-build/triggers
- Build Logs: https://console.cloud.google.com/logs/query

## Customization

### Update Substitutions

Edit the trigger substitutions or pass them at runtime:

```bash
gcloud builds submit --config=.cloudbuild/staging.yaml \
  --substitutions=_STAGING_PROJECT_ID=new-project,_REGION=us-east1
```

### Modify Build Steps

Edit the YAML files to add custom steps:

```yaml
steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: custom-step
    entrypoint: /bin/bash
    args:
      - '-c'
      - |
        echo "Custom logic here"
```

### Add Notifications

Configure Pub/Sub notifications for build events:

```bash
# Create topic
gcloud pubsub topics create cloud-builds --project=YOUR_CICD_PROJECT_ID

# Subscribe Cloud Build notifications
gcloud builds triggers update deploy-staging \
  --project=YOUR_CICD_PROJECT_ID \
  --pubsub-topic=projects/YOUR_CICD_PROJECT_ID/topics/cloud-builds
```

## Troubleshooting

### Build Fails with Permission Errors

Check that the Cloud Build service account has necessary permissions:

```bash
# Check IAM bindings
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:*@cloudbuild.gserviceaccount.com"
```

### Deployment Timeouts

Increase the timeout in the YAML file:

```yaml
timeout: 3600s  # 60 minutes
```

### Agent Engine Deployment Fails

Verify the Agent Engine API is enabled:

```bash
gcloud services enable aiplatform.googleapis.com \
  --project=YOUR_STAGING_PROJECT_ID
```

### Load Tests Not Running

Ensure the load test file exists:

```bash
ls -la tests/load_test/load_test.py
```

## Best Practices

1. **Use Substitutions**: Never hardcode project IDs or regions
2. **Enable Logs Bucket**: Always configure a logs bucket for audit trails
3. **Set Timeouts**: Configure appropriate timeouts for each pipeline
4. **Manual Approval for Prod**: Always require approval for production deployments
5. **Monitor Error Rates**: Use health checks to catch issues early
6. **Save Artifacts**: Preserve deployment records and test results
7. **Rollback Plan**: Document rollback procedures for each deployment

## Related Documentation

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Build Triggers](https://cloud.google.com/build/docs/triggers)
- [Agent Starter Pack Deployment Patterns](../docs/analysis/03_deploy_patterns.md)
- [GitHub Actions Alternative](../.github/workflows/README.md)

## Support

For issues or questions:
1. Check build logs in Cloud Console
2. Review Agent Starter Pack documentation
3. Check GCP status page for service issues
4. Contact your DevOps team
