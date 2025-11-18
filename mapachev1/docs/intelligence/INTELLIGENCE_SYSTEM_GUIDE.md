# Mapache Continuous Intelligence System

## Overview

The Mapache Continuous Intelligence System is a Google Cloud-native platform that autonomously discovers, analyzes, and synthesizes AI/ML content from 35+ sources, creating actionable Linear projects every morning at 6 AM CET.

**Key Features:**
- 🔍 Continuous content scraping (48x/day) from HackerNews, Reddit, ProductHunt, ArXiv, GitHub, and major AI blogs
- 🧠 Gemini-powered relevance analysis and strategic synthesis
- 📋 Automatic Linear project creation with complete specifications
- 📬 Daily Slack briefings with top opportunities
- 🚀 100% Google Cloud native (no third-party orchestration)
- 💰 Cost-optimized (~$121/month)

## Architecture

### Components

1. **Scraping Layer**
   - 6 Cloud Run Jobs (one per source type)
   - Parallel execution via Cloud Workflows
   - Triggered every 30 minutes by Cloud Scheduler
   - Raw content stored in GCS and published to Pub/Sub

2. **Processing Layer**
   - Cloud Function triggered by Pub/Sub
   - Gemini 2.0 Flash for content analysis
   - Relevance scoring (0-100)
   - Structured storage in Firestore

3. **Intelligence Layer**
   - Chief Agent (Vertex AI + Gemini)
   - Daily synthesis of top opportunities
   - Linear project creation via GraphQL API
   - Slack notifications via webhooks

4. **Orchestration**
   - Cloud Workflows for scraper coordination
   - Cloud Scheduler for timing
   - Eventarc for event-driven triggers
   - Secret Manager for credentials

## Data Flow

```
Every 30 min:
Cloud Scheduler → Cloud Workflows → 6 Cloud Run Jobs (parallel)
                                    ↓
                            Publish to Pub/Sub
                                    ↓
                            Cloud Function (analysis)
                                    ↓
                            Firestore (storage)

Daily at 6 AM CET:
Cloud Scheduler → Chief Agent Cloud Function
                  ↓
                  Query Firestore (relevance ≥ 70)
                  ↓
                  Gemini synthesis
                  ↓
                  Create 3-7 Linear projects
                  ↓
                  Send Slack briefing
```

## Quick Start

### Prerequisites

- Google Cloud SDK installed and configured
- Active GCP project with billing enabled
- Linear account with API access
- Slack workspace with webhook configured
- GitHub, Reddit, ProductHunt API tokens (optional but recommended)

### Deployment

1. **Clone and navigate:**
   ```bash
   cd mapachev1
   ```

2. **Configure environment:**
   ```bash
   export GCP_PROJECT_ID="your-project-id"
   export GCP_REGION="europe-west1"
   ```

3. **Run deployment:**
   ```bash
   ./deployment/intelligence/deploy.sh
   ```

   This will:
   - Enable required GCP APIs
   - Create Pub/Sub topics and subscriptions
   - Set up GCS buckets and Firestore
   - Build and deploy 6 Cloud Run Jobs
   - Deploy 2 Cloud Functions
   - Configure Cloud Workflows
   - Create Cloud Scheduler jobs (paused)

4. **Configure secrets:**
   ```bash
   # Linear API key
   echo -n "YOUR_LINEAR_API_KEY" | \
     gcloud secrets versions add linear-api-key --data-file=-

   # Slack webhook
   echo -n "YOUR_SLACK_WEBHOOK_URL" | \
     gcloud secrets versions add slack-webhook-url --data-file=-

   # Reddit OAuth (optional)
   echo -n "YOUR_REDDIT_CLIENT_ID" | \
     gcloud secrets versions add reddit-client-id --data-file=-
   echo -n "YOUR_REDDIT_SECRET" | \
     gcloud secrets versions add reddit-client-secret --data-file=-

   # GitHub token (optional)
   echo -n "YOUR_GITHUB_TOKEN" | \
     gcloud secrets versions add github-token --data-file=-

   # ProductHunt token (optional)
   echo -n "YOUR_PRODUCTHUNT_TOKEN" | \
     gcloud secrets versions add producthunt-api-token --data-file=-
   ```

5. **Test manually:**
   ```bash
   # Test scraping workflow
   gcloud workflows execute intelligence-orchestrator \
     --location=europe-west1

   # Wait 5 minutes, check Firestore
   gcloud firestore documents list discoveries --limit=10

   # Test Chief Agent
   CHIEF_URL=$(gcloud functions describe intelligence-chief-agent \
     --region=europe-west1 \
     --format="value(serviceConfig.uri)")
   curl -X POST $CHIEF_URL
   ```

6. **Enable schedulers:**
   ```bash
   # Enable scraping every 30 minutes
   gcloud scheduler jobs resume scraping-orchestrator \
     --location=europe-west1

   # Enable daily briefing at 6 AM CET
   gcloud scheduler jobs resume chief-agent-daily-trigger \
     --location=europe-west1
   ```

## Content Sources

### HackerNews
- Top stories API
- AI-filtered by keywords
- Score and comment count metadata

### Reddit
- 7 AI/ML subreddits
- OAuth authentication
- Hot posts with engagement data

### ProductHunt
- Daily AI product launches
- GraphQL API
- Vote and comment counts

### Blogs (RSS)
- Google Cloud AI/ML Blog
- Anthropic News
- OpenAI Blog
- LangChain Blog
- HuggingFace Blog
- DeepMind Blog

### ArXiv
- cs.AI, cs.CL, cs.LG, cs.NE, stat.ML
- Last 7 days of papers
- Full abstracts and metadata

### GitHub
- Key AI framework releases
- Anthropic, OpenAI, Google, LangChain, etc.
- Release notes and changelogs

## Gemini Analysis

Each piece of content is analyzed with the following prompt structure:

```
Analyze content and provide:
1. Relevance Score (0-100)
2. Strategic Value (1-2 sentences)
3. Key Insights (2-4 bullets)
4. Action Items (2-3 concrete steps)
5. Tags (3-5 categorization tags)
```

**Thresholds:**
- ≥ 60: Store in Firestore
- ≥ 70: Include in Chief Agent analysis
- ≥ 80: High-priority opportunities

## Chief Agent

The Chief Agent runs daily at 6 AM CET and:

1. **Queries Firestore** for discoveries with relevance ≥ 70
2. **Synthesizes** top 5-7 strategic opportunities
3. **Creates Linear projects** with:
   - Clear, actionable title
   - Comprehensive description
   - Technical requirements (bulleted)
   - Acceptance criteria (bulleted)
   - Rollback plan
   - Priority level (low/medium/high/urgent)
4. **Sends Slack briefing** with:
   - Daily summary
   - Discovery statistics
   - Links to all created projects
   - Top opportunities overview

## Monitoring

### Cloud Console

**Logs:**
```bash
# Scraper logs
gcloud logging read 'resource.type=cloud_run_job' --limit=50

# Cloud Function logs
gcloud logging read 'resource.type=cloud_function' --limit=50

# Workflow logs
gcloud logging read 'resource.type=workflows.googleapis.com/workflow' --limit=20
```

**Metrics:**
- Cloud Console → Cloud Run Jobs → intelligence-scraper-*
- Cloud Console → Cloud Functions → intelligence-*
- Cloud Console → Workflows → intelligence-orchestrator

**Firestore:**
```bash
# Check discovery count
gcloud firestore documents list discoveries | wc -l

# View recent discoveries
gcloud firestore documents list discoveries --limit=10
```

### Alerts

Set up alerts for:
- Cloud Run Job failures (3+ consecutive failures)
- Cloud Function errors (5+ errors in 10 minutes)
- Workflow execution failures
- Firestore write quota exceeded

## Costs

### Monthly Estimate (~$121)

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run Jobs | 6 × 48 runs/day | $15 |
| Cloud Workflows | 48 executions/day | $0.50 |
| Pub/Sub | 10K messages/day | $5 |
| Cloud Functions | 10K invocations/day | $5 |
| Gemini (analysis) | 500 requests/day | $20 |
| Gemini (Chief Agent) | 30 queries/day | $10 |
| Firestore | 1M reads, 50K writes | $25 |
| GCS | 10GB storage | $0.20 |
| Cloud Scheduler | 2 jobs | $1 |
| **Total** | | **~$81.70/month** |

**Note:** Actual costs may vary. Monitor Cloud Console → Billing.

## Troubleshooting

### Scraper Not Running

```bash
# Check Cloud Scheduler status
gcloud scheduler jobs describe scraping-orchestrator --location=europe-west1

# Check Workflow execution
gcloud workflows executions list intelligence-orchestrator --location=europe-west1

# Check Cloud Run Job logs
gcloud logging read 'resource.type=cloud_run_job' --limit=20
```

### No Discoveries in Firestore

```bash
# Check if Pub/Sub messages are being published
gcloud pubsub topics list

# Check Cloud Function logs
gcloud logging read 'resource.type=cloud_function' --limit=20

# Manually trigger analyzer
gcloud functions call intelligence-content-analyzer \
  --data='{"message":{"data":"..."}}'
```

### Chief Agent Not Creating Projects

```bash
# Check if Chief Agent is being triggered
gcloud scheduler jobs describe chief-agent-daily-trigger --location=europe-west1

# Check Cloud Function logs
gcloud logging read 'resource.labels.function_name=intelligence-chief-agent' --limit=10

# Verify Linear API key
gcloud secrets versions access latest --secret=linear-api-key

# Manually trigger
curl -X POST $(gcloud functions describe intelligence-chief-agent \
  --region=europe-west1 --format="value(serviceConfig.uri)")
```

### API Rate Limits

If you hit rate limits:
- **HackerNews:** No auth required, very generous limits
- **Reddit:** Add OAuth credentials to Secret Manager
- **GitHub:** Add personal access token to Secret Manager
- **ProductHunt:** Add API token to Secret Manager

## Customization

### Add New Content Source

1. Create scraper in `app/intelligence/scrapers/`:
   ```python
   from .base import BaseScraper

   class NewScraper(BaseScraper):
       def __init__(self):
           super().__init__("newsource")

       def scrape(self):
           # Your scraping logic
           return [RawContent(...)]
   ```

2. Create Dockerfile in `deployment/intelligence/cloud_run/`

3. Update `deploy.sh` to include new scraper

4. Update Cloud Workflows to add new job

### Adjust Relevance Threshold

Edit `app/intelligence/utils/config.py`:

```python
relevance_threshold: int = 60  # Minimum for storage
project_threshold: int = 70    # Minimum for Chief Agent
```

### Change Scraping Frequency

```bash
gcloud scheduler jobs update http scraping-orchestrator \
  --schedule="*/15 * * * *" \  # Every 15 minutes
  --location=europe-west1
```

### Modify Chief Agent Schedule

```bash
gcloud scheduler jobs update http chief-agent-daily-trigger \
  --schedule="0 8 * * *" \  # 8 AM instead of 6 AM
  --location=europe-west1
```

## Backup and Recovery

### Firestore Backup

```bash
# Export Firestore
gcloud firestore export gs://mapache-intelligence-backups/$(date +%Y%m%d)

# Import Firestore
gcloud firestore import gs://mapache-intelligence-backups/YYYYMMDD
```

### GCS Lifecycle

Raw content in GCS is automatically deleted after 90 days (lifecycle policy).

To adjust:
```bash
gsutil lifecycle set lifecycle.json gs://mapache-intelligence-raw-content
```

## Security

### IAM Permissions

Cloud Run Jobs and Functions use default service account:
- Pub/Sub Publisher
- Firestore User
- Storage Object Creator
- Secret Manager Secret Accessor
- Vertex AI User

### Secret Rotation

Rotate secrets regularly:
```bash
# Create new version
echo -n "NEW_SECRET_VALUE" | \
  gcloud secrets versions add SECRET_NAME --data-file=-

# Delete old versions
gcloud secrets versions destroy VERSION_ID --secret=SECRET_NAME
```

## Support

For issues:
1. Check logs in Cloud Console
2. Review Firestore for data issues
3. Verify Secret Manager credentials
4. Test components individually
5. Check Cloud Scheduler job status

## Next Steps

1. Monitor first 24 hours of operation
2. Review Firestore discoveries for quality
3. Check first Linear projects for accuracy
4. Tune relevance thresholds if needed
5. Add additional content sources as needed
6. Set up custom alerting rules

---

**Built with Google Cloud Native services for maximum reliability and scalability.**
