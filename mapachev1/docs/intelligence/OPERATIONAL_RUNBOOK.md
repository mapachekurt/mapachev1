# Mapache Intelligence System - Operational Runbook

## Daily Operations

### Morning Routine (6:10 AM CET)

**What Happens:**
- Chief Agent analyzes overnight discoveries
- Creates 3-7 Linear projects automatically
- Sends Slack notification to your phone

**Your Actions (5-10 minutes):**

1. **Check Slack notification** (30 seconds)
   - View daily summary
   - Note discovery count
   - Check project count

2. **Open Linear** (1 minute)
   - Navigate to newly created projects
   - All will be in your default team

3. **For each project** (1-2 minutes per project):
   - **Option A - Approve:** Assign to Claude Code (web) or Google Jules
   - **Option B - Modify:** Edit specifications before assignment
   - **Option C - Archive:** Delete if not relevant

4. **Optional - Adjust system:**
   - Too many low-quality projects? Increase relevance threshold
   - Missing opportunities? Decrease relevance threshold
   - Wrong focus? Update Chief Agent instructions

### Weekly Review (30 minutes on Fridays)

1. **Quality Assessment:**
   ```bash
   # Check discoveries this week
   gcloud firestore documents list discoveries --limit=100
   ```
   - Are sources providing value?
   - Any irrelevant content getting through?
   - Missing any important topics?

2. **Cost Review:**
   - Cloud Console → Billing
   - Expected: ~$4/day = ~$121/month
   - Alert if trending > $150/month

3. **Project Outcomes:**
   - Review Linear projects created this week
   - Track which ones led to value
   - Identify patterns in successful projects

4. **System Tuning:**
   - Adjust relevance thresholds if needed
   - Add/remove content sources
   - Update Chief Agent instructions
   - Modify scraping frequency if needed

## Common Tasks

### Check System Health

```bash
# Check if scrapers are running
gcloud scheduler jobs list --location=europe-west1

# View recent workflow executions
gcloud workflows executions list intelligence-orchestrator \
  --location=europe-west1 --limit=5

# Check for errors in last hour
gcloud logging read 'severity>=ERROR' \
  --freshness=1h \
  --limit=20
```

### Manual Scraping Run

```bash
# Trigger scraping workflow now
gcloud workflows execute intelligence-orchestrator \
  --location=europe-west1

# Monitor execution
gcloud workflows executions describe EXECUTION_ID \
  --workflow=intelligence-orchestrator \
  --location=europe-west1
```

### Manual Chief Agent Run

```bash
# Get Cloud Function URL
CHIEF_URL=$(gcloud functions describe intelligence-chief-agent \
  --region=europe-west1 \
  --format="value(serviceConfig.uri)")

# Trigger Chief Agent
curl -X POST $CHIEF_URL

# Check logs
gcloud logging read \
  'resource.labels.function_name=intelligence-chief-agent' \
  --limit=10
```

### View Recent Discoveries

```bash
# List recent discoveries
gcloud firestore documents list discoveries --limit=20

# Query high-relevance discoveries
gcloud firestore documents list discoveries \
  --filter="relevance_score>=80" \
  --limit=10
```

### Update API Credentials

```bash
# Linear API key
echo -n "NEW_LINEAR_KEY" | \
  gcloud secrets versions add linear-api-key --data-file=-

# Slack webhook
echo -n "NEW_SLACK_WEBHOOK" | \
  gcloud secrets versions add slack-webhook-url --data-file=-

# Verify update
gcloud secrets versions list linear-api-key
```

## Troubleshooting Scenarios

### Scenario 1: No Slack Notification Received

**Symptoms:**
- 6:10 AM passes, no Slack message
- Expected daily briefing missing

**Diagnosis:**

1. Check if Chief Agent ran:
   ```bash
   gcloud logging read \
     'resource.labels.function_name=intelligence-chief-agent' \
     --limit=5
   ```

2. Check Cloud Scheduler:
   ```bash
   gcloud scheduler jobs describe chief-agent-daily-trigger \
     --location=europe-west1
   ```

3. Verify Slack webhook:
   ```bash
   gcloud secrets versions access latest --secret=slack-webhook-url
   ```

**Solutions:**

- If scheduler is paused: Resume it
  ```bash
  gcloud scheduler jobs resume chief-agent-daily-trigger \
    --location=europe-west1
  ```

- If webhook is wrong: Update it
  ```bash
  echo -n "CORRECT_WEBHOOK" | \
    gcloud secrets versions add slack-webhook-url --data-file=-
  ```

- If no discoveries: Check Firestore
  ```bash
  gcloud firestore documents list discoveries --limit=10
  ```

### Scenario 2: Scrapers Not Running

**Symptoms:**
- No new discoveries in Firestore
- GCS bucket not updating

**Diagnosis:**

1. Check scheduler status:
   ```bash
   gcloud scheduler jobs describe scraping-orchestrator \
     --location=europe-west1
   ```

2. Check workflow executions:
   ```bash
   gcloud workflows executions list intelligence-orchestrator \
     --location=europe-west1 --limit=5
   ```

3. Check Cloud Run Job logs:
   ```bash
   gcloud logging read 'resource.type=cloud_run_job' --limit=20
   ```

**Solutions:**

- If scheduler paused: Resume
  ```bash
  gcloud scheduler jobs resume scraping-orchestrator \
    --location=europe-west1
  ```

- If workflow failing: Check logs and re-deploy
  ```bash
  gcloud workflows deploy intelligence-orchestrator \
    --source=deployment/intelligence/workflows/intelligence-orchestrator.yaml \
    --location=europe-west1
  ```

- If jobs failing: Redeploy specific scraper
  ```bash
  gcloud run jobs update intelligence-scraper-hackernews \
    --image=gcr.io/PROJECT_ID/intelligence-scraper-hackernews:latest \
    --region=europe-west1
  ```

### Scenario 3: Low-Quality Projects Being Created

**Symptoms:**
- Too many irrelevant Linear projects
- Projects don't align with strategy

**Solutions:**

1. **Increase relevance threshold:**
   - Edit `app/intelligence/utils/config.py`
   - Change `project_threshold` from 70 to 80
   - Redeploy Chief Agent function

2. **Update Chief Agent instructions:**
   - Edit `app/intelligence/chief_agent/agent.py`
   - Modify `SYNTHESIS_PROMPT` to be more specific
   - Redeploy Chief Agent function

3. **Filter content sources:**
   - Remove low-value sources from scrapers
   - Redeploy affected scraper jobs

### Scenario 4: API Rate Limits

**Symptoms:**
- Scraper logs show 429 errors
- Some sources not returning data

**Solutions:**

1. **GitHub:**
   ```bash
   # Add personal access token
   echo -n "ghp_YOUR_TOKEN" | \
     gcloud secrets versions add github-token --data-file=-
   ```

2. **Reddit:**
   ```bash
   # Add OAuth credentials
   echo -n "CLIENT_ID" | \
     gcloud secrets versions add reddit-client-id --data-file=-
   echo -n "CLIENT_SECRET" | \
     gcloud secrets versions add reddit-client-secret --data-file=-
   ```

3. **ProductHunt:**
   ```bash
   # Add API token
   echo -n "API_TOKEN" | \
     gcloud secrets versions add producthunt-api-token --data-file=-
   ```

### Scenario 5: High Costs

**Symptoms:**
- Daily billing > $6
- Monthly projection > $150

**Diagnosis:**

1. Check cost breakdown:
   - Cloud Console → Billing → Cost Table
   - Identify highest-cost service

2. Common causes:
   - Too many Gemini API calls
   - High Firestore read/write volume
   - Excessive Cloud Run executions

**Solutions:**

1. **Reduce scraping frequency:**
   ```bash
   gcloud scheduler jobs update http scraping-orchestrator \
     --schedule="0 */2 * * *" \  # Every 2 hours instead of 30 min
     --location=europe-west1
   ```

2. **Increase relevance threshold:**
   - Fewer items stored = lower Firestore costs
   - Edit config, set `relevance_threshold` to 70 or 80

3. **Optimize Gemini calls:**
   - Truncate content before analysis
   - Already done in analyzer (2000 chars max)

## Maintenance Tasks

### Monthly

1. **Review and archive old discoveries:**
   ```bash
   # Delete discoveries older than 30 days
   # (Create a Cloud Function for this)
   ```

2. **Rotate secrets:**
   ```bash
   # Update Linear API key
   echo -n "NEW_KEY" | \
     gcloud secrets versions add linear-api-key --data-file=-

   # Delete old versions
   gcloud secrets versions destroy VERSION_ID --secret=linear-api-key
   ```

3. **Review cost trends:**
   - Cloud Console → Billing → Reports
   - Look for unexpected increases
   - Adjust if trending above budget

### Quarterly

1. **Evaluate content sources:**
   - Which sources provide most value?
   - Any new sources to add?
   - Any sources to remove?

2. **Update scraper dependencies:**
   ```bash
   cd mapachev1
   uv add package@latest
   ./deployment/intelligence/deploy.sh --skip-infrastructure
   ```

3. **Review and update Chief Agent:**
   - Is it creating valuable projects?
   - Any patterns in rejected projects?
   - Update instructions if needed

### Annually

1. **Full system review:**
   - Architecture still optimal?
   - Any new GCP services to leverage?
   - Cost optimization opportunities?

2. **Dependency updates:**
   ```bash
   cd mapachev1
   uv update
   ./deployment/intelligence/deploy.sh
   ```

## Emergency Procedures

### Complete System Shutdown

```bash
# Pause all schedulers
gcloud scheduler jobs pause scraping-orchestrator --location=europe-west1
gcloud scheduler jobs pause chief-agent-daily-trigger --location=europe-west1

# Stop in-flight executions (if needed)
gcloud workflows executions cancel EXECUTION_ID \
  --workflow=intelligence-orchestrator \
  --location=europe-west1
```

### Complete System Restart

```bash
# Resume schedulers
gcloud scheduler jobs resume scraping-orchestrator --location=europe-west1
gcloud scheduler jobs resume chief-agent-daily-trigger --location=europe-west1

# Trigger immediate run to verify
gcloud workflows execute intelligence-orchestrator --location=europe-west1
```

### Rollback Deployment

```bash
# Redeploy from specific commit
git checkout GOOD_COMMIT_HASH
cd mapachev1
./deployment/intelligence/deploy.sh

# Or redeploy specific component
gcloud run jobs update intelligence-scraper-hackernews \
  --image=gcr.io/PROJECT_ID/intelligence-scraper-hackernews:PREVIOUS_TAG \
  --region=europe-west1
```

## Monitoring Dashboard URLs

**Cloud Console:**
- Cloud Run Jobs: https://console.cloud.google.com/run/jobs?project=PROJECT_ID
- Cloud Functions: https://console.cloud.google.com/functions/list?project=PROJECT_ID
- Cloud Scheduler: https://console.cloud.google.com/cloudscheduler?project=PROJECT_ID
- Firestore: https://console.cloud.google.com/firestore/data?project=PROJECT_ID
- Logs: https://console.cloud.google.com/logs?project=PROJECT_ID
- Billing: https://console.cloud.google.com/billing?project=PROJECT_ID

## Contacts and Escalation

**For GCP issues:**
- Google Cloud Support (if you have a support plan)
- Stack Overflow: `google-cloud-platform` tag

**For scraping issues:**
- Check API status pages:
  - GitHub: https://www.githubstatus.com/
  - Reddit: https://www.redditstatus.com/
  - ProductHunt: Check their Twitter

**For Linear issues:**
- Linear API docs: https://developers.linear.app/docs
- Linear support: support@linear.app

## Success Metrics

**Daily:**
- Discoveries scraped: 50-200
- High-relevance discoveries (≥70): 10-50
- Linear projects created: 3-7
- Slack notification sent: ✓

**Weekly:**
- Approved projects: ≥5
- Projects leading to value: ≥2
- System uptime: >99%
- Cost: <$35/week

**Monthly:**
- Total discoveries: 1,500-6,000
- Total projects created: 80-200
- Projects shipped: ≥10
- Cost: <$150

---

**Remember:** The system is designed to reduce your time investment to 5-10 minutes per day. If you're spending more time than that, something needs tuning!
