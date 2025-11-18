# Mapache Continuous Intelligence System

**Autonomous AI-powered content discovery and opportunity synthesis**

## What It Does

The Mapache Intelligence System continuously:
- 🔍 **Discovers** AI/ML content from 35+ sources (48x/day)
- 🧠 **Analyzes** content with Gemini AI for relevance and strategic value
- 📋 **Creates** complete Linear projects for top opportunities
- 📬 **Delivers** daily Slack briefings every morning at 6 AM CET

**Your time investment: 5-10 minutes per day** to review and approve projects.

## Quick Start

### 1. Deploy

```bash
cd mapachev1
./deployment/intelligence/deploy.sh
```

### 2. Configure Secrets

```bash
# Linear API key
echo -n "YOUR_LINEAR_KEY" | gcloud secrets versions add linear-api-key --data-file=-

# Slack webhook
echo -n "YOUR_SLACK_WEBHOOK" | gcloud secrets versions add slack-webhook-url --data-file=-
```

### 3. Enable

```bash
# Enable scraping (every 30 min)
gcloud scheduler jobs resume scraping-orchestrator --location=europe-west1

# Enable daily briefing (6 AM CET)
gcloud scheduler jobs resume chief-agent-daily-trigger --location=europe-west1
```

### 4. Test

```bash
# Trigger a scraping run
gcloud workflows execute intelligence-orchestrator --location=europe-west1

# Trigger Chief Agent
curl -X POST $(gcloud functions describe intelligence-chief-agent \
  --region=europe-west1 --format="value(serviceConfig.uri)")
```

## Architecture

100% Google Cloud Native:
- **Cloud Run Jobs** for parallel scraping
- **Cloud Workflows** for orchestration
- **Pub/Sub** for event-driven processing
- **Cloud Functions** for Gemini analysis
- **Firestore** for structured storage
- **Vertex AI** for Chief Agent
- **Cloud Scheduler** for timing

**No third-party orchestration. No maintenance overhead.**

## Content Sources

- **HackerNews:** AI-filtered top stories
- **Reddit:** 7 AI/ML subreddits
- **ProductHunt:** AI product launches
- **Blogs:** Google Cloud, Anthropic, OpenAI, LangChain, HuggingFace, DeepMind
- **ArXiv:** Latest AI/ML research papers
- **GitHub:** Key AI framework releases

## Cost

**~$87/month** (well under $150 budget)

Breakdown:
- Cloud Run Jobs: $15
- Gemini API: $30
- Firestore: $25
- Cloud Functions: $10
- Pub/Sub: $5
- Other: $2

## Documentation

- **[Complete Implementation Guide](./INTELLIGENCE_SYSTEM_GUIDE.md)** - Full technical details
- **[Operational Runbook](./OPERATIONAL_RUNBOOK.md)** - Day-to-day operations
- **[Quick Reference](./QUICK_REFERENCE.md)** - Commands and troubleshooting

## Support

**Check system status:**
```bash
gcloud scheduler jobs list --location=europe-west1
```

**View recent discoveries:**
```bash
gcloud firestore documents list discoveries --limit=10
```

**Check logs:**
```bash
gcloud logging read 'severity>=ERROR' --freshness=1h --limit=10
```

## Daily Workflow

**Morning (6:10 AM):**
1. Receive Slack notification
2. Open Linear
3. Review 3-7 new projects
4. Assign to Claude Code or Google Jules

**That's it. 5-10 minutes per day.**

## Customization

**Adjust relevance threshold** (fewer/more projects):
- Edit `app/intelligence/utils/config.py`
- Change `project_threshold` (default: 70)

**Change scraping frequency:**
```bash
gcloud scheduler jobs update http scraping-orchestrator \
  --schedule="0 */2 * * *" --location=europe-west1
```

**Add new content source:**
1. Create scraper in `app/intelligence/scrapers/`
2. Add Dockerfile in `deployment/intelligence/cloud_run/`
3. Update `deploy.sh`

## Monitoring

**Cloud Console Dashboards:**
- [Cloud Run Jobs](https://console.cloud.google.com/run/jobs)
- [Cloud Functions](https://console.cloud.google.com/functions/list)
- [Firestore](https://console.cloud.google.com/firestore/data)
- [Logs](https://console.cloud.google.com/logs/query)
- [Billing](https://console.cloud.google.com/billing)

## Troubleshooting

**No Slack notification?**
```bash
gcloud scheduler jobs describe chief-agent-daily-trigger --location=europe-west1
```

**No discoveries?**
```bash
gcloud logging read 'resource.type=cloud_run_job' --limit=20
```

**High costs?**
```bash
# Check billing
gcloud billing accounts list

# Reduce frequency
gcloud scheduler jobs update http scraping-orchestrator \
  --schedule="0 */2 * * *" --location=europe-west1
```

## Success Metrics

**Daily:**
- 50-200 discoveries scraped
- 10-50 high-relevance discoveries (≥70)
- 3-7 Linear projects created

**Weekly:**
- ≥5 approved projects
- ≥2 projects leading to value
- >99% uptime

**Monthly:**
- 1,500-6,000 total discoveries
- 80-200 projects created
- ≥10 projects shipped
- <$150 cost

---

**Built to operate at the speed of AI, not the speed of human reading.**

🚀 **Deploy once. Review daily. Scale infinitely.**
