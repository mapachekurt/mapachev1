# Deployment Guide - Agent Improvements Framework

**Version:** 1.0.0
**Last Updated:** 2025-11-17
**Audience:** DevOps Engineers, SREs, Engineering Leads

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Deployment Options](#deployment-options)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Configuration Management](#configuration-management)
6. [Health Checks & Monitoring](#health-checks--monitoring)
7. [Rollback Procedures](#rollback-procedures)
8. [Post-Deployment Validation](#post-deployment-validation)
9. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying to production, ensure all items are completed:

### Testing ✓
- [ ] All unit tests passing (`pytest tests/unit/`)
- [ ] Integration tests passing (`pytest tests/integration/`)
- [ ] Test coverage ≥ 85%
- [ ] Load testing completed (100 RPS sustained)
- [ ] Smoke tests validated

### Code Quality ✓
- [ ] Code linted (`ruff check src/`)
- [ ] Type checking passed (`mypy src/`)
- [ ] No security vulnerabilities (`bandit -r src/`)
- [ ] Code reviewed by at least 2 engineers

### Configuration ✓
- [ ] All config files validated (`config/*.yaml`)
- [ ] Environment variables set
- [ ] Secrets managed in Secret Manager
- [ ] API keys rotated and secured

### Documentation ✓
- [ ] README.md updated
- [ ] ARCHITECTURE.md reviewed
- [ ] Runbooks created for on-call
- [ ] Rollback procedure documented

### Quality Gates ✓
- [ ] Golden task pass rate ≥ 95%
- [ ] P95 latency ≤ 5000ms
- [ ] Cost per request ≤ $0.10
- [ ] Error rate ≤ 1%

---

## Environment Setup

### Prerequisites

**Required:**
- Python 3.10-3.12
- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Docker (for local SLM)

**Optional:**
- Redis (can use fakeredis for testing)
- Kubernetes cluster (for GKE deployment)

### Installation

**Development/Staging:**
```bash
# Clone repository
git clone https://github.com/mapachekurt/mapachev1.git
cd mapachev1

# Install with development dependencies
uv pip install -e ".[dev,lint]"

# Or with pip
pip install -e ".[dev,lint]"
```

**Production:**
```bash
# Install only production dependencies
uv pip install -e ".[prod]"

# Or with pip
pip install -e ".[prod]"
```

### Environment Variables

Create `.env` file:

```bash
# Google Cloud
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Observability
export LOG_LEVEL="INFO"
export ENABLE_STRUCTURED_LOGGING="true"
export ENABLE_TRACING="true"
export METRICS_PORT="9090"

# Cost Optimization
export ENABLE_CACHING="true"
export ENABLE_LOCAL_SLM="true"
export REDIS_URL="redis://localhost:6379"

# Deployment
export ENVIRONMENT="production"  # development, staging, production
export SERVICE_VERSION="1.0.0"
```

---

## Deployment Options

### Option 1: Google Cloud Run (Recommended for Serverless)

**Pros:**
- Auto-scaling (0 to N)
- Pay-per-use
- Managed infrastructure
- Fast deployments

**Cons:**
- Cold starts
- Request timeout limits (60 minutes max)

**Best For:** Event-driven agents, low-volume workloads

### Option 2: Google Kubernetes Engine (GKE)

**Pros:**
- Full control
- No cold starts
- Advanced networking
- Stateful workloads

**Cons:**
- More complex
- Always-on costs
- Requires K8s expertise

**Best For:** High-volume production, 511+ agents

### Option 3: Vertex AI Agent Engine

**Pros:**
- Native Google ADK integration
- Managed scaling
- Built-in observability

**Cons:**
- Less flexibility
- Higher cost

**Best For:** Pure ADK agents, minimal customization

### Option 4: Local/On-Premises

**Pros:**
- Full control
- No cloud costs
- Data sovereignty

**Cons:**
- Manual scaling
- Infrastructure management
- Limited Google Cloud integration

**Best For:** Development, testing, compliance requirements

---

## Step-by-Step Deployment

### Phase 1: Initial Setup (Week 1)

**1.1 Create GCP Resources**

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable \
  aiplatform.googleapis.com \
  logging.googleapis.com \
  cloudtrace.googleapis.com \
  run.googleapis.com

# Create service account
gcloud iam service-accounts create agent-service \
  --display-name="Agent Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:agent-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

**1.2 Deploy to Cloud Run**

```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/agent-improvements:1.0.0

# Deploy
gcloud run deploy agent-improvements \
  --image gcr.io/YOUR_PROJECT_ID/agent-improvements:1.0.0 \
  --platform managed \
  --region us-central1 \
  --service-account agent-service@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --concurrency 100 \
  --max-instances 10 \
  --set-env-vars "ENVIRONMENT=production,LOG_LEVEL=INFO"
```

### Phase 2: Enable Observability (Week 2)

**2.1 Configure Logging**

```yaml
# config/observability.yaml
logging:
  enabled: true
  level: INFO
  output:
    cloud_logging: true  # Enable Cloud Logging
```

**2.2 Configure Tracing**

```yaml
# config/observability.yaml
tracing:
  enabled: true
  exporters:
    - cloud_trace  # Enable Cloud Trace
```

**2.3 Create Dashboards**

```bash
# Import dashboards to Cloud Monitoring
python scripts/import_dashboards.py
```

### Phase 3: Enable Cost Optimization (Week 3)

**3.1 Deploy Local SLM (Optional)**

```bash
# Start Ollama with Docker
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama:latest

# Pull model
docker exec ollama ollama pull llama3.2:3b
```

**3.2 Enable Caching**

```bash
# Deploy Redis
gcloud redis instances create agent-cache \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_7_0

# Get Redis connection
gcloud redis instances describe agent-cache \
  --region=us-central1 \
  --format='get(host)'
```

### Phase 4: Deploy All 511 Agents (Week 4-5)

**4.1 Bulk Deployment Script**

```python
# scripts/deploy_all_agents.py
import asyncio
from pathlib import Path

async def deploy_agent(agent_path):
    """Deploy single agent with improvements."""
    # Add observability
    # Add cost tracking
    # Add reliability patterns
    # Deploy to Cloud Run
    pass

async def deploy_all():
    """Deploy all 511 agents."""
    agent_dirs = Path("agents/saas_agents").glob("*/")
    tasks = [deploy_agent(d) for d in agent_dirs]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(deploy_all())
```

**4.2 Progressive Rollout**

```bash
# Deploy to 1% of traffic (canary)
gcloud run services update-traffic agent-improvements \
  --to-revisions=agent-improvements-v2=1

# Monitor for 1 hour
# If metrics good, increase to 10%
gcloud run services update-traffic agent-improvements \
  --to-revisions=agent-improvements-v2=10

# Continue: 25% → 50% → 100%
```

---

## Configuration Management

### Development

```yaml
# config/development.yaml
environment: development
enable_debug: true
cost_tracking:
  enabled: false
observability:
  sampling_rate: 1.0
```

### Staging

```yaml
# config/staging.yaml
environment: staging
enable_debug: false
cost_tracking:
  enabled: true
  budgets:
    daily: 100  # $100/day for testing
observability:
  sampling_rate: 1.0
```

### Production

```yaml
# config/production.yaml
environment: production
enable_debug: false
cost_tracking:
  enabled: true
  budgets:
    daily: 1000  # $1000/day
    monthly: 25000
observability:
  sampling_rate: 0.1  # 10% sampling
```

---

## Health Checks & Monitoring

### Health Endpoints

```python
# Implement in your service
@app.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/health/ready")
async def readiness_check():
    """Readiness check with dependencies."""
    checks = {
        "database": await check_db(),
        "redis": await check_redis(),
        "llm_api": await check_llm_api(),
    }
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    raise HTTPException(status_code=503, detail="Not ready")
```

### Monitoring Alerts

**Critical Alerts:**
- Error rate > 5%
- Success rate < 90%
- P95 latency > 10 seconds
- Cost spike > 50%
- Service down for > 5 minutes

**Warning Alerts:**
- Error rate > 1%
- Success rate < 95%
- P95 latency > 5 seconds
- Cost increase > 20%
- Low cache hit rate < 30%

### SLOs (Service Level Objectives)

```yaml
availability:
  target: 99.9%
  window: 30 days

latency:
  p50: 1000ms
  p95: 5000ms
  p99: 10000ms

error_rate:
  target: < 1%
  window: 1 hour

cost:
  target: < $0.10 per request
  window: 1 day
```

---

## Rollback Procedures

### Automatic Rollback

**Triggers:**
- Success rate < 90% for 5 minutes
- Error rate > 10% for 5 minutes
- P99 latency > 30 seconds

**Actions:**
```bash
# Automatic rollback via monitoring
gcloud run services update-traffic agent-improvements \
  --to-revisions=agent-improvements-v1=100
```

### Manual Rollback

**Step 1: Identify Issue**
```bash
# Check recent deployments
gcloud run revisions list \
  --service=agent-improvements \
  --region=us-central1

# Check logs
gcloud logging read "resource.type=cloud_run_revision AND \
  resource.labels.service_name=agent-improvements" \
  --limit=100
```

**Step 2: Roll Back**
```bash
# Route all traffic to previous version
gcloud run services update-traffic agent-improvements \
  --to-revisions=agent-improvements-v1=100

# Or delete problematic revision
gcloud run revisions delete agent-improvements-v2 \
  --region=us-central1
```

**Step 3: Verify**
```bash
# Check traffic distribution
gcloud run services describe agent-improvements \
  --region=us-central1 \
  --format="get(status.traffic)"

# Run smoke tests
python scripts/run_smoke_tests.py
```

---

## Post-Deployment Validation

### Smoke Tests

```bash
# Run comprehensive smoke tests
python scripts/run_smoke_tests.py --env production

# Expected output:
# ✓ Health endpoint: PASS
# ✓ Authentication: PASS
# ✓ Basic agent call: PASS
# ✓ Cost tracking: PASS
# ✓ Logging: PASS
# ✓ Metrics: PASS
```

### Load Testing

```bash
# Run load test
python scripts/load_test.py \
  --url https://agent-improvements-abc123.run.app \
  --rps 100 \
  --duration 600

# Expected metrics:
# - P50 latency: < 1000ms
# - P95 latency: < 5000ms
# - P99 latency: < 10000ms
# - Success rate: > 99%
# - Error rate: < 1%
```

### Golden Task Validation

```bash
# Run golden tasks against production
python -m src.evaluation.executor \
  --config config/golden_tasks.yaml \
  --environment production

# Expected pass rate: ≥ 95%
```

---

## Troubleshooting

### Issue: High Latency

**Symptoms:**
- P95 latency > 5 seconds
- Slow response times

**Diagnosis:**
```bash
# Check Cloud Trace
gcloud trace list --limit=100

# Check for slow LLM calls
gcloud logging read "jsonPayload.duration_ms > 5000"
```

**Solutions:**
- Enable caching
- Use local SLM for routine tasks
- Increase concurrency
- Optimize prompt sizes

### Issue: High Costs

**Symptoms:**
- Daily cost > budget
- Cost per request > $0.10

**Diagnosis:**
```python
# Check cost breakdown
from src.optimization import CostTracker
tracker = CostTracker()
stats = tracker.get_stats()
print(f"Top spenders: {tracker.get_top_spenders(limit=10)}")
```

**Solutions:**
- Enable semantic caching
- Route simple queries to local SLM
- Use cheaper models (GPT-3.5 vs GPT-4)
- Set stricter budgets

### Issue: Circuit Breaker Open

**Symptoms:**
- CircuitBreakerOpenError exceptions
- Service unavailable

**Diagnosis:**
```python
# Check circuit breaker status
from src.reliability import CircuitBreaker
cb = CircuitBreaker()
print(f"State: {cb.state}, Failures: {cb.failure_count}")
```

**Solutions:**
- Wait for timeout (60 seconds default)
- Fix underlying service issue
- Reset circuit breaker manually
- Adjust failure threshold

### Issue: Memory Leaks

**Symptoms:**
- Memory usage increasing over time
- OOM kills

**Diagnosis:**
```bash
# Monitor memory
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container/memory/utilizations"'
```

**Solutions:**
- Enable memory consolidation
- Set TTLs on sessions
- Clear old vector memories
- Restart service periodically

---

## Production Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation complete
- [ ] Team trained
- [ ] On-call rotation set
- [ ] Rollback plan tested

### Launch Day
- [ ] Deploy to 1% canary
- [ ] Monitor for 1 hour
- [ ] Gradual rollout (1% → 10% → 25% → 50% → 100%)
- [ ] Validate metrics at each stage
- [ ] Run smoke tests
- [ ] Update status page

### Post-Launch
- [ ] Monitor for 24 hours
- [ ] Review logs and metrics
- [ ] Adjust alerting thresholds
- [ ] Document lessons learned
- [ ] Schedule retrospective

---

## Next Steps

1. **Week 1-2:** Deploy to staging, validate all features
2. **Week 3:** Canary deployment to production (1% traffic)
3. **Week 4:** Progressive rollout to 100%
4. **Week 5:** Monitor and optimize
5. **Week 6+:** Continuous improvement

---

## Support

**Documentation:**
- [README.md](README.md) - Quick start
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Integration steps
- [GAP_ANALYSIS.md](GAP_ANALYSIS.md) - Before/after metrics

**On-Call:**
- Slack: #agent-ops
- PagerDuty: agent-improvements-team
- Runbook: [internal wiki link]

**Emergency Contacts:**
- Engineering Lead: [contact]
- SRE On-Call: [contact]
- Product Owner: [contact]

---

**Document Version:** 1.0.0
**Last Review:** 2025-11-17
**Next Review:** 2025-12-17
