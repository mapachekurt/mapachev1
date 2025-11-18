# Intelligence System - Quick Reference

## Essential Commands

### Check System Status
```bash
# All schedulers
gcloud scheduler jobs list --location=europe-west1

# Recent workflow executions
gcloud workflows executions list intelligence-orchestrator --location=europe-west1 --limit=5

# Recent errors
gcloud logging read 'severity>=ERROR' --freshness=1h --limit=10
```

### Manual Triggers
```bash
# Trigger scraping now
gcloud workflows execute intelligence-orchestrator --location=europe-west1

# Trigger Chief Agent now
curl -X POST $(gcloud functions describe intelligence-chief-agent --region=europe-west1 --format="value(serviceConfig.uri)")
```

### View Data
```bash
# Recent discoveries
gcloud firestore documents list discoveries --limit=10

# High-relevance only
gcloud firestore documents list discoveries --filter="relevance_score>=80" --limit=10
```

### Update Secrets
```bash
# Linear
echo -n "NEW_KEY" | gcloud secrets versions add linear-api-key --data-file=-

# Slack
echo -n "NEW_WEBHOOK" | gcloud secrets versions add slack-webhook-url --data-file=-
```

## Architecture Map

```
┌─────────────────┐
│ Cloud Scheduler │ Every 30 min
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Workflows │ Parallel orchestration
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│ 6 Cloud Run Jobs (Scrapers)                │
│ • HackerNews  • Reddit  • ProductHunt       │
│ • Blogs       • ArXiv   • GitHub            │
└────────┬────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│    Pub/Sub      │ Event bus
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Function  │ Gemini analysis
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Firestore     │ Structured storage
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Scheduler │ Daily 6 AM CET
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chief Agent    │ Vertex AI + Gemini
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
    ┌────────┐    ┌────────┐
    │ Linear │    │ Slack  │
    └────────┘    └────────┘
```

## Key Configurations

### Relevance Thresholds
- **Storage:** 60 (minimum to save in Firestore)
- **Projects:** 70 (minimum for Chief Agent consideration)
- **High Priority:** 80+ (urgent opportunities)

**Location:** `app/intelligence/utils/config.py`

### Schedules
- **Scraping:** Every 30 minutes (`*/30 * * * *`)
- **Chief Agent:** Daily at 6 AM CET (`0 6 * * *`)

**Location:** Cloud Scheduler jobs

### Content Sources (6 Scrapers)

| Scraper | Sources | Update Frequency |
|---------|---------|------------------|
| HackerNews | Top 50 stories | Every 30 min |
| Reddit | 7 AI/ML subreddits | Every 30 min |
| ProductHunt | AI products | Every 30 min |
| Blogs | 6 major AI blogs | Every 30 min |
| ArXiv | 5 AI/ML categories | Every 30 min |
| GitHub | 8 key repositories | Every 30 min |

## Cost Breakdown

| Component | Monthly Cost |
|-----------|--------------|
| Cloud Run Jobs | $15 |
| Cloud Functions | $10 |
| Gemini API | $30 |
| Firestore | $25 |
| Pub/Sub | $5 |
| Other | $2 |
| **Total** | **~$87** |

**Target:** < $150/month
**Alert if:** > $200/month

## Troubleshooting Matrix

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| No Slack notification | Scheduler paused | `gcloud scheduler jobs resume chief-agent-daily-trigger --location=europe-west1` |
| No new discoveries | Scraper paused | `gcloud scheduler jobs resume scraping-orchestrator --location=europe-west1` |
| Low-quality projects | Threshold too low | Increase `project_threshold` to 80 in config |
| Too few projects | Threshold too high | Decrease `project_threshold` to 60 in config |
| API rate limits | Missing auth tokens | Add tokens to Secret Manager |
| High costs | Too frequent scraping | Change schedule to `0 */2 * * *` (every 2 hrs) |

## File Locations

```
mapachev1/
├── app/intelligence/
│   ├── scrapers/
│   │   ├── hackernews.py
│   │   ├── reddit.py
│   │   ├── producthunt.py
│   │   ├── blogs.py
│   │   ├── arxiv.py
│   │   └── github.py
│   ├── processors/
│   │   ├── gemini_analyzer.py
│   │   └── cloud_function_main.py
│   ├── chief_agent/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── cloud_function_main.py
│   └── utils/
│       ├── config.py
│       ├── models.py
│       ├── pubsub_client.py
│       └── gcs_client.py
├── deployment/intelligence/
│   ├── deploy.sh
│   ├── requirements.txt
│   ├── cloud_run/
│   │   └── Dockerfile.*
│   └── workflows/
│       └── intelligence-orchestrator.yaml
└── docs/intelligence/
    ├── INTELLIGENCE_SYSTEM_GUIDE.md
    ├── OPERATIONAL_RUNBOOK.md
    └── QUICK_REFERENCE.md (this file)
```

## Environment Variables

**GCP Project:**
```bash
export GCP_PROJECT_ID="mapache-intelligence-prod"
export GCP_REGION="europe-west1"
```

**Set in Cloud Functions/Jobs:**
- `GCP_PROJECT_ID`: Project ID
- `GCP_REGION`: Deployment region

**Retrieved from Secret Manager:**
- `LINEAR_API_KEY`: Linear API token
- `SLACK_WEBHOOK_URL`: Slack webhook URL
- `REDDIT_CLIENT_ID`: Reddit OAuth client ID
- `REDDIT_CLIENT_SECRET`: Reddit OAuth secret
- `GITHUB_TOKEN`: GitHub personal access token
- `PRODUCTHUNT_API_TOKEN`: ProductHunt API token

## Monitoring URLs

**Dashboards:**
- [Cloud Run Jobs](https://console.cloud.google.com/run/jobs)
- [Cloud Functions](https://console.cloud.google.com/functions/list)
- [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler)
- [Firestore](https://console.cloud.google.com/firestore/data)
- [Logs Explorer](https://console.cloud.google.com/logs/query)
- [Billing](https://console.cloud.google.com/billing)

**Log Filters:**
```
# All intelligence system logs
resource.labels.service_name=~"intelligence-*"

# Errors only
severity>=ERROR AND resource.labels.service_name=~"intelligence-*"

# Scraper logs
resource.type="cloud_run_job"

# Chief Agent logs
resource.labels.function_name="intelligence-chief-agent"
```

## Daily Workflow

**6:00 AM CET:** System analyzes overnight discoveries
**6:05 AM CET:** Linear projects created
**6:10 AM CET:** Slack notification sent

**Your Actions:**
1. Check Slack (30 sec)
2. Open Linear (1 min)
3. Review projects (1-2 min each)
4. Assign/modify/archive (total: 5-10 min)

**Done!** System handles the rest automatically.

## Quick Deploy

```bash
# Full deployment
cd mapachev1
./deployment/intelligence/deploy.sh

# Update secrets
echo -n "LINEAR_KEY" | gcloud secrets versions add linear-api-key --data-file=-
echo -n "SLACK_WEBHOOK" | gcloud secrets versions add slack-webhook-url --data-file=-

# Enable schedulers
gcloud scheduler jobs resume scraping-orchestrator --location=europe-west1
gcloud scheduler jobs resume chief-agent-daily-trigger --location=europe-west1
```

## Emergency Stop

```bash
# Pause everything
gcloud scheduler jobs pause scraping-orchestrator --location=europe-west1
gcloud scheduler jobs pause chief-agent-daily-trigger --location=europe-west1
```

## Emergency Restart

```bash
# Resume everything
gcloud scheduler jobs resume scraping-orchestrator --location=europe-west1
gcloud scheduler jobs resume chief-agent-daily-trigger --location=europe-west1
```

---

**For detailed information, see:**
- [Complete Implementation Guide](./INTELLIGENCE_SYSTEM_GUIDE.md)
- [Operational Runbook](./OPERATIONAL_RUNBOOK.md)
