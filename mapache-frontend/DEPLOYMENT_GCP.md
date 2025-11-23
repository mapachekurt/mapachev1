# Google Cloud Platform Deployment Guide
## Mapache Frontend

This guide provides detailed instructions for deploying the Mapache frontend to Google Cloud Platform.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Deploy](#quick-deploy)
- [Detailed Deployment Options](#detailed-deployment-options)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Install Google Cloud SDK

```bash
# macOS
brew install --cask google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Windows
# Download from: https://cloud.google.com/sdk/docs/install
```

### 2. Authenticate and Configure

```bash
# Login to GCP
gcloud auth login

# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  containerregistry.googleapis.com \
  secretmanager.googleapis.com
```

### 3. Set Environment Variables

```bash
# Backend URL (replace with your actual backend URL)
export BACKEND_URL="https://your-backend-service.run.app"
export WS_URL="wss://your-backend-service.run.app/ws"
```

---

## Quick Deploy

The fastest way to deploy to Cloud Run:

```bash
cd mapache-frontend

gcloud run deploy mapache-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
  --set-env-vars="NEXT_PUBLIC_WS_URL=${WS_URL}"
```

This will:
1. Build your container using Cloud Build
2. Push to Container Registry
3. Deploy to Cloud Run
4. Return your service URL

---

## Detailed Deployment Options

### Option 1: Cloud Run with Source Deploy

**Best for:** Quick iterations, automatic builds

```bash
cd mapache-frontend

# Deploy with environment variables
gcloud run deploy mapache-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
  --set-env-vars="NEXT_PUBLIC_WS_URL=${WS_URL}" \
  --set-env-vars="NEXT_TELEMETRY_DISABLED=1"
```

### Option 2: Manual Docker Build & Deploy

**Best for:** Custom builds, more control

**Step 1: Build locally**
```bash
# Build the Docker image
docker build -t gcr.io/${PROJECT_ID}/mapache-frontend:latest .

# Test locally
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=${BACKEND_URL} \
  -e NEXT_PUBLIC_WS_URL=${WS_URL} \
  gcr.io/${PROJECT_ID}/mapache-frontend:latest
```

**Step 2: Push to GCR**
```bash
# Configure Docker authentication
gcloud auth configure-docker

# Push image
docker push gcr.io/${PROJECT_ID}/mapache-frontend:latest
```

**Step 3: Deploy to Cloud Run**
```bash
gcloud run deploy mapache-frontend \
  --image gcr.io/${PROJECT_ID}/mapache-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: CI/CD with Cloud Build

**Best for:** Production deployments, automated pipelines

**Step 1: Create Cloud Build trigger**
```bash
gcloud builds triggers create github \
  --name="mapache-frontend-deploy" \
  --repo-name=mapachev1 \
  --repo-owner=mapachekurt \
  --branch-pattern="^main$" \
  --build-config=mapache-frontend/cloudbuild.yaml \
  --included-files="mapache-frontend/**" \
  --substitutions="_BACKEND_URL=${BACKEND_URL},_WS_URL=${WS_URL}"
```

**Step 2: Manual trigger (optional)**
```bash
gcloud builds submit \
  --config=mapache-frontend/cloudbuild.yaml \
  --substitutions=_BACKEND_URL=${BACKEND_URL},_WS_URL=${WS_URL} \
  mapache-frontend/
```

---

## Configuration

### Environment Variables

#### Method 1: Direct Environment Variables

```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
  --set-env-vars="NEXT_PUBLIC_WS_URL=${WS_URL}" \
  --set-env-vars="NEXT_PUBLIC_AUTH_ENABLED=true" \
  --set-env-vars="NEXT_PUBLIC_ANALYTICS_ENABLED=true"
```

#### Method 2: Using Secret Manager (Recommended for Sensitive Data)

**Create secrets:**
```bash
# Create API URL secret
echo -n "${BACKEND_URL}" | \
  gcloud secrets create mapache-api-url --data-file=-

# Create WebSocket URL secret
echo -n "${WS_URL}" | \
  gcloud secrets create mapache-ws-url --data-file=-

# Create auth token secret (if needed)
echo -n "your-auth-token" | \
  gcloud secrets create mapache-auth-token --data-file=-
```

**Grant Cloud Run access:**
```bash
# Get the service account email
export SERVICE_ACCOUNT=$(gcloud run services describe mapache-frontend \
  --region us-central1 \
  --format="value(spec.template.spec.serviceAccountName)")

# Grant access to secrets
gcloud secrets add-iam-policy-binding mapache-api-url \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding mapache-ws-url \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

**Update service to use secrets:**
```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --update-secrets=NEXT_PUBLIC_API_URL=mapache-api-url:latest \
  --update-secrets=NEXT_PUBLIC_WS_URL=mapache-ws-url:latest
```

### Custom Domain

**Step 1: Verify domain ownership**
```bash
gcloud domains verify mapache.app
```

**Step 2: Map domain to Cloud Run**
```bash
gcloud run domain-mappings create \
  --service mapache-frontend \
  --domain mapache.app \
  --region us-central1
```

**Step 3: Update DNS records**
Follow the instructions provided by GCP to add the required DNS records to your domain registrar.

### SSL/TLS Certificates

Cloud Run automatically provisions and manages SSL certificates for custom domains. No additional configuration needed!

---

## Monitoring

### View Logs

**Real-time logs:**
```bash
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend"
```

**Recent logs:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend" \
  --limit 100 \
  --format json
```

**Error logs only:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend AND severity>=ERROR" \
  --limit 50
```

### Metrics & Monitoring

**Cloud Console:**
Visit: https://console.cloud.google.com/run/detail/us-central1/mapache-frontend/metrics

**Key metrics to monitor:**
- Request count
- Request latency (p50, p95, p99)
- Error rate
- Container instance count
- CPU utilization
- Memory utilization

**Create alerts:**
```bash
# Alert on high error rate
gcloud alpha monitoring policies create \
  --notification-channels=YOUR_CHANNEL_ID \
  --display-name="Mapache Frontend High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=5 \
  --condition-threshold-duration=300s
```

### Performance Monitoring

Enable Cloud Trace for detailed performance insights:

```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --set-env-vars="ENABLE_TRACING=true"
```

---

## Scaling Configuration

### Auto-scaling

```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 100 \
  --concurrency 80
```

### Resource Limits

```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300
```

### Traffic Splitting (Blue/Green Deployments)

```bash
# Deploy new revision
gcloud run deploy mapache-frontend \
  --image gcr.io/${PROJECT_ID}/mapache-frontend:v2 \
  --no-traffic

# Split traffic (90% old, 10% new)
gcloud run services update-traffic mapache-frontend \
  --to-revisions=LATEST=10,mapache-frontend-00001=90

# Gradually increase to new version
gcloud run services update-traffic mapache-frontend \
  --to-latest
```

---

## Cost Optimization

### 1. Set appropriate min/max instances

```bash
# For development
gcloud run services update mapache-frontend \
  --min-instances 0 \
  --max-instances 5

# For production
gcloud run services update mapache-frontend \
  --min-instances 1 \
  --max-instances 50
```

### 2. Use appropriate resource allocation

```bash
# Start conservative
gcloud run services update mapache-frontend \
  --memory 512Mi \
  --cpu 1

# Scale up if needed based on metrics
```

### 3. Enable request-based billing

Cloud Run charges only for:
- Requests (free tier: 2M requests/month)
- CPU time (free tier: 360,000 vCPU-seconds/month)
- Memory time (free tier: 180,000 GiB-seconds/month)

---

## Troubleshooting

### Common Issues

**1. Build fails with "permission denied"**
```bash
# Grant Cloud Build service account necessary permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"
```

**2. Service fails to start**
```bash
# Check logs for errors
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend AND severity>=ERROR" \
  --limit 50

# Check service configuration
gcloud run services describe mapache-frontend \
  --region us-central1
```

**3. Environment variables not set**
```bash
# Verify environment variables
gcloud run services describe mapache-frontend \
  --region us-central1 \
  --format="value(spec.template.spec.containers[0].env)"
```

**4. CORS errors when connecting to backend**
```bash
# Ensure backend allows frontend origin
# Add to your backend CORS configuration:
# - https://mapache-frontend-xxxxx.run.app
# - https://mapache.app (if using custom domain)
```

**5. High latency**
```bash
# Check cold start times
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend AND textPayload=~'cold start'" \
  --limit 20

# Consider setting min-instances > 0
gcloud run services update mapache-frontend \
  --min-instances 1
```

### Health Checks

```bash
# Test the deployed service
export SERVICE_URL=$(gcloud run services describe mapache-frontend \
  --region us-central1 \
  --format="value(status.url)")

curl -I ${SERVICE_URL}
```

### Rollback to Previous Revision

```bash
# List revisions
gcloud run revisions list --service mapache-frontend --region us-central1

# Rollback to specific revision
gcloud run services update-traffic mapache-frontend \
  --to-revisions=mapache-frontend-00001=100
```

---

## Production Checklist

Before going to production:

- [ ] Set appropriate min/max instances
- [ ] Configure custom domain with SSL
- [ ] Set up Cloud Monitoring alerts
- [ ] Configure Secret Manager for sensitive data
- [ ] Enable Cloud Trace for performance monitoring
- [ ] Set up Cloud Build triggers for CI/CD
- [ ] Configure CORS on backend
- [ ] Test auto-scaling under load
- [ ] Set up Cloud Armor for DDoS protection (if needed)
- [ ] Configure Cloud CDN (if needed)
- [ ] Review and optimize resource allocation
- [ ] Set up backup/disaster recovery plan
- [ ] Configure log retention policies

---

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Next.js on Cloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-nodejs-service)
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)

---

## Support

For issues specific to:
- **Mapache Frontend**: Create issue on GitHub
- **Google Cloud Platform**: [GCP Support](https://cloud.google.com/support)
- **Next.js**: [Next.js Documentation](https://nextjs.org/docs)
