# Staging Deployment Scripts

Comprehensive staging deployment scripts for the Agent Production Framework with all 7 critical improvements.

## Overview

This directory contains production-ready scripts for deploying, testing, validating, and managing the staging environment.

## Scripts

### 1. setup_staging.sh (376 lines)
**Purpose**: Initial setup of the staging environment

**What it does**:
- Creates all required GCP resources (Cloud Run, Redis, Secret Manager)
- Sets up IAM service accounts with proper permissions
- Enables required APIs
- Builds and deploys the initial container image
- Creates monitoring dashboards

**Usage**:
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1  # optional, defaults to us-central1

./deployment/staging/setup_staging.sh
```

**Prerequisites**:
- gcloud CLI installed and authenticated
- GCP project with billing enabled
- Appropriate IAM permissions

---

### 2. run_smoke_tests.sh (493 lines)
**Purpose**: Run comprehensive smoke tests against staging

**What it tests**:
- ✓ Health endpoint (HTTP 200, healthy status)
- ✓ Metrics endpoint (Prometheus format)
- ✓ Basic agent functionality (execution endpoint)
- ✓ Observability (logging, tracing, metrics)
- ✓ Cost tracking (budgets, alerts)
- ✓ All 7 improvements:
  1. Evaluation Framework (golden tasks)
  2. Observability Layer (logging, tracing, metrics)
  3. Memory System (session & vector memory)
  4. Agent Coordination (message broker)
  5. Cost Optimization (LLM router, cache)
  6. Reliability Patterns (circuit breaker)
  7. Production Operations (deployments, health checks)
- ✓ End-to-end workflow with all improvements
- ✓ Service performance (response time)

**Usage**:
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

./deployment/staging/run_smoke_tests.sh
```

**Exit Codes**:
- `0`: All tests passed
- `1`: One or more tests failed

**Example Output**:
```
[INFO] Starting smoke tests for staging environment...
[TEST] Testing health endpoint...
[PASS] Health endpoint returned 200 OK
[PASS] Health endpoint returned healthy status
...
Total Tests:  16
Passed:       16
Failed:       0
```

---

### 3. deploy_pilot_agents.sh (781 lines)
**Purpose**: Deploy 2 pilot agents to staging with all 7 improvements

**What it does**:
- Selects 2 pilot agents from `agents/saas_agents/`
  - Agent 1: `contentful` (Content Marketing)
  - Agent 2: `zendesk` (Customer Support)
- Enhances each agent with all 7 improvements:
  1. **Evaluation Framework** - Golden tasks, quality gates, validators
  2. **Observability Layer** - Structured logging, distributed tracing, metrics
  3. **Memory System** - Session memory (short-term), vector memory (long-term)
  4. **Agent Coordination** - A2A protocol, message broker, orchestration
  5. **Cost Optimization** - LLM router, local SLM support, result cache
  6. **Reliability Patterns** - Circuit breaker, retry, timeout, bulkhead
  7. **Production Operations** - Health checks, smoke tests, deployments
- Deploys enhanced agents to staging
- Runs validation tests
- Generates deployment report

**Usage**:
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

./deployment/staging/deploy_pilot_agents.sh
```

**Output Files**:
- `/tmp/pilot_agents_*/` - Enhanced agent code
- `/tmp/pilot_deployment_*.log` - Deployment log
- `/tmp/pilot_agents_*/deployment_report.txt` - Deployment report

**Example Output**:
```
[STEP] Enhancing agent: contentful with all 7 improvements...
[INFO] [contentful] Adding Improvement #1: Evaluation Framework...
[INFO] [contentful] Adding Improvement #2: Observability Layer...
...
[SUCCESS] [contentful] Enhanced with all 7 improvements
[SUCCESS] [contentful] Deployed to staging
```

---

### 4. validate_staging.sh (641 lines)
**Purpose**: Comprehensive validation of the staging environment

**What it validates**:

**Section 1: GCP Resources**
- Cloud Run service exists and is deployed
- Service account exists with correct IAM roles
- Redis instance exists and is READY
- Secret Manager secrets exist
- Required APIs are enabled

**Section 2: Configuration**
- Environment variables are configured
- Resource allocation (memory, CPU)
- Scaling configuration (min/max instances)
- Local configuration files exist

**Section 3: Service Health**
- Health endpoint responding
- Metrics endpoint functional
- Service generating logs
- No recent errors in logs
- Service latency is acceptable

**Section 4: Golden Tasks**
- Golden task execution functional
- Sample tasks pass validation
- Golden tasks configuration exists
- Quality gates defined for all environments

**Section 5: Monitoring & Observability**
- Cloud Logging integration
- Cloud Trace integration
- Cloud Monitoring integration
- Observability configuration exists

**Usage**:
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

./deployment/staging/validate_staging.sh
```

**Exit Codes**:
- `0`: All checks passed (may have warnings)
- `1`: Critical issues found

**Output**:
- Validation report saved to `/tmp/staging_validation_*.txt`

**Example Output**:
```
[CHECK] Validating Cloud Run service...
[PASS] Cloud Run service exists and is deployed
[CHECK] Validating service account...
[PASS] Service account exists: agent-staging@project.iam.gserviceaccount.com
...
Total Checks:    45
Passed:          42
Failed:          0
Warnings:        3

Status: ✓ HEALTHY - Staging environment is ready for use
```

---

### 5. rollback_staging.sh (463 lines)
**Purpose**: Rollback staging deployment if issues are found

**What it does**:
- Confirms rollback with user (unless auto-confirm enabled)
- Identifies current and previous revisions
- Captures current state for audit trail
- Routes 100% traffic to previous stable version
- Tests service health after rollback
- Preserves failed revision for investigation
- Generates rollback report
- Prepares team notification
- Creates incident report

**Usage**:
```bash
export GCP_PROJECT_ID=your-project-id
export GCP_REGION=us-central1

# Interactive rollback (asks for confirmation)
./deployment/staging/rollback_staging.sh "Failed health checks"

# Automated rollback (no confirmation)
ROLLBACK_AUTO_CONFIRM=true ./deployment/staging/rollback_staging.sh "Automated rollback due to errors"
```

**Arguments**:
- `$1` (optional): Rollback reason (default: "Manual rollback requested")

**Environment Variables**:
- `ROLLBACK_AUTO_CONFIRM`: Set to `true` to skip confirmation prompt

**Output Files**:
- `/tmp/rollback_*.log` - Rollback execution log
- `/tmp/rollback_report_*.txt` - Detailed rollback report
- `/tmp/rollback_notification_*.txt` - Team notification message
- `/tmp/incident_*.json` - Incident report in JSON format

**Example Output**:
```
[WARN] ROLLBACK CONFIRMATION REQUIRED
Service: agent-improvements-staging
Reason: Failed health checks

Do you want to proceed with rollback? (yes/no): yes

[STEP] Routing traffic to previous stable version...
[SUCCESS] Traffic successfully routed to previous revision
[STEP] Testing service health after rollback...
[SUCCESS] Service health check passed (HTTP 200)

✓ Rollback completed successfully!
```

---

## Common Workflows

### Initial Setup
```bash
# 1. Set up staging environment
export GCP_PROJECT_ID=my-project
./deployment/staging/setup_staging.sh

# 2. Validate environment
./deployment/staging/validate_staging.sh

# 3. Run smoke tests
./deployment/staging/run_smoke_tests.sh
```

### Deploy Pilot Agents
```bash
# 1. Deploy pilot agents with all improvements
./deployment/staging/deploy_pilot_agents.sh

# 2. Run smoke tests to verify
./deployment/staging/run_smoke_tests.sh

# 3. Validate everything is working
./deployment/staging/validate_staging.sh
```

### Rollback if Issues Found
```bash
# If smoke tests fail or issues are detected
./deployment/staging/rollback_staging.sh "Smoke tests failed"
```

### Regular Health Checks
```bash
# Quick health check
./deployment/staging/run_smoke_tests.sh

# Comprehensive validation
./deployment/staging/validate_staging.sh
```

---

## Environment Variables

All scripts support the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GCP_PROJECT_ID` | Yes | - | GCP project ID |
| `GCP_REGION` | No | `us-central1` | GCP region for resources |
| `ROLLBACK_AUTO_CONFIRM` | No | `false` | Auto-confirm rollback (rollback_staging.sh only) |

---

## Script Features

All scripts include:

- **Colored Output**: GREEN (info/pass), YELLOW (warn), RED (error), BLUE (step)
- **Error Handling**: `set -euo pipefail` for safe execution
- **Logging**: All actions logged to timestamped files
- **Exit Codes**: Proper exit codes for CI/CD integration
- **Validation**: Prerequisite checks before execution
- **Reports**: Comprehensive reports for audit and debugging

---

## Troubleshooting

### "GCP_PROJECT_ID environment variable not set"
```bash
export GCP_PROJECT_ID=your-project-id
```

### "Service not found"
```bash
# Run setup first
./deployment/staging/setup_staging.sh
```

### "Health checks failing"
```bash
# Check logs
gcloud run logs read agent-improvements-staging \
  --region=us-central1 \
  --project=$GCP_PROJECT_ID

# Validate environment
./deployment/staging/validate_staging.sh
```

### "Smoke tests failing"
```bash
# Run validation to identify issues
./deployment/staging/validate_staging.sh

# Check specific service endpoints
SERVICE_URL=$(gcloud run services describe agent-improvements-staging \
  --region=us-central1 \
  --project=$GCP_PROJECT_ID \
  --format="get(status.url)")

curl $SERVICE_URL/health
curl $SERVICE_URL/metrics
```

### "Rollback needed"
```bash
# Rollback to previous stable version
./deployment/staging/rollback_staging.sh "Issue description"
```

---

## Integration with CI/CD

All scripts are designed to work in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Deploy to Staging
  run: ./deployment/staging/setup_staging.sh
  env:
    GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}

- name: Run Smoke Tests
  run: ./deployment/staging/run_smoke_tests.sh
  env:
    GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}

- name: Rollback on Failure
  if: failure()
  run: |
    ROLLBACK_AUTO_CONFIRM=true \
    ./deployment/staging/rollback_staging.sh "CI/CD smoke tests failed"
  env:
    GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
```

---

## Total Lines of Code

| Script | Lines | Purpose |
|--------|-------|---------|
| setup_staging.sh | 376 | Initial staging setup |
| run_smoke_tests.sh | 493 | Comprehensive smoke tests |
| deploy_pilot_agents.sh | 781 | Deploy pilot agents with improvements |
| validate_staging.sh | 641 | Environment validation |
| rollback_staging.sh | 463 | Deployment rollback |
| **Total** | **2,754** | **Complete staging automation** |

---

## Support

For issues or questions:
1. Check the validation report: `./deployment/staging/validate_staging.sh`
2. Review logs in `/tmp/` directory
3. Check GCP Console for resource status
4. Review DEPLOYMENT_GUIDE.md for detailed deployment information

---

## Next Steps

After successful staging deployment:
1. Monitor staging metrics for 24-48 hours
2. Run golden tasks to validate agent quality
3. Prepare production deployment plan
4. Update remaining 509 agents with improvements
5. Roll out to production

See DEPLOYMENT_GUIDE.md for production deployment instructions.
