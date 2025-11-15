# Agent Starter Pack - Best Practices Summary

> **Synthesized from comprehensive analysis of GoogleCloudPlatform/agent-starter-pack**
> **Date:** 2025-11-14
> **Analysis Source:** Docs 01-05 in this directory

## Table of Contents

1. [Project Structure Standards](#project-structure-standards)
2. [Configuration Management Best Practices](#configuration-management-best-practices)
3. [Testing and Evaluation Strategies](#testing-and-evaluation-strategies)
4. [Infrastructure as Code Patterns](#infrastructure-as-code-patterns)
5. [CI/CD Best Practices](#cicd-best-practices)
6. [Security and Compliance Requirements](#security-and-compliance-requirements)
7. [Multi-Agent System Design Principles](#multi-agent-system-design-principles)
8. [Observability and Monitoring](#observability-and-monitoring)
9. [Production Readiness Checklist](#production-readiness-checklist)

---

## 1. Project Structure Standards

### Standard Directory Layout

```
project-root/
├── app/                          # Core application code
│   ├── agent.py                  # Main agent definition (MUST export 'agent' variable)
│   ├── agent_engine_app.py       # Agent Engine deployment wrapper
│   ├── agents/                   # Multi-agent systems
│   │   ├── coordinators/         # High-level routing agents
│   │   ├── teams/                # Mid-level team agents
│   │   └── specialists/          # Leaf-level specialist agents
│   ├── tools/                    # Custom tool implementations
│   └── app_utils/                # Utilities (tracing, logging, helpers)
│       └── tracing.py            # OpenTelemetry instrumentation
├── deployment/                    # Infrastructure as code
│   ├── terraform/                # All Terraform configurations
│   │   ├── providers.tf          # Multi-project provider setup
│   │   ├── variables.tf          # Input variables
│   │   ├── locals.tf             # Computed values
│   │   ├── service_accounts.tf   # SA definitions
│   │   ├── iam.tf                # Role bindings
│   │   ├── apis.tf               # API enablement
│   │   ├── storage.tf            # GCS, Artifact Registry, Vector Search
│   │   ├── log_sinks.tf          # BigQuery log routing
│   │   └── outputs.tf            # Export values for CI/CD
│   └── README.md                 # Deployment documentation
├── .github/workflows/            # GitHub Actions CI/CD
│   ├── pr.yaml                   # PR validation
│   ├── deploy-staging.yaml       # Auto-deploy to staging on merge
│   └── deploy-prod.yaml          # Manual prod deployment
├── .cloudbuild/                  # Cloud Build CI/CD (alternative)
│   ├── pr.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── tests/                        # All test code
│   ├── unit/                     # Unit tests for agents/tools
│   ├── integration/              # Multi-agent workflow tests
│   ├── load/                     # Load testing with Locust
│   └── e2e/                      # End-to-end deployment tests
├── notebooks/                    # Jupyter notebooks for prototyping
│   ├── 01_prototype_agent.ipynb  # Local development
│   └── 02_evaluate_agent.ipynb   # Vertex AI Evaluation
├── docs/                         # Project documentation
│   ├── analysis/                 # Design analysis
│   ├── architecture/             # Architecture diagrams
│   └── runbooks/                 # Operational guides
├── Makefile                      # Standard commands (install, test, deploy)
├── pyproject.toml                # Project metadata and dependencies
├── uv.lock                       # Locked dependencies
├── GEMINI.md                     # AI-assisted development context
├── README.md                     # Project overview
└── .env.example                  # Environment variable template
```

### Key Principles

1. **Single Source of Truth**: `app/agent.py` must export `agent` variable for ADK discovery
2. **Separation of Concerns**: Tools, agents, and utilities in separate modules
3. **Multi-Environment Support**: Same code deploys to dev/staging/prod via configuration
4. **Infrastructure as Code**: All resources defined in Terraform
5. **Observability First**: Tracing and logging instrumented from day one

---

## 2. Configuration Management Best Practices

### Environment-Specific Configuration

Use **Terraform variables** for environment differences:

```hcl
# deployment/terraform/variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "min_instances" {
  description = "Minimum Cloud Run instances"
  type        = number
  default     = 0  # Dev/staging: 0, Prod: 1 for zero cold-start
}

variable "max_instances" {
  description = "Maximum Cloud Run instances"
  type        = number
  default     = 10  # Dev: 5, Staging: 10, Prod: 100
}
```

### Application Configuration

Use **environment variables** with `.env` files:

```bash
# .env.example
PROJECT_ID=your-gcp-project-id
REGION=us-central1
AGENT_ENGINE_ID=projects/.../reasoningEngines/...
LOG_LEVEL=INFO
TRACE_SAMPLE_RATE=1.0  # Dev: 1.0, Prod: 0.1
```

### Secret Management

**DO:**
- Store secrets in **Google Secret Manager**
- Reference secrets in Terraform with `google_secret_manager_secret_version`
- Use service account-based access (no API keys)
- Rotate secrets regularly

**DON'T:**
- Commit secrets to Git (`.env` in `.gitignore`)
- Hardcode credentials in code
- Share service account keys

---

## 3. Testing and Evaluation Strategies

### Test Pyramid

```
        ┌─────────────┐
        │  E2E Tests  │  (5%)  - Full deployment validation
        ├─────────────┤
        │ Integration │  (20%) - Multi-agent workflows
        │    Tests    │
        ├─────────────┤
        │ Unit Tests  │  (75%) - Individual agent/tool logic
        └─────────────┘
```

### Unit Tests (75% of tests)

```python
# tests/unit/test_agents/test_sales_agent.py
import pytest
from app.agents.sales_agent import sales_agent

@pytest.mark.asyncio
async def test_sales_agent_handles_lead_query():
    """Test that sales agent correctly routes lead generation requests."""
    result = await sales_agent.run("Find me 10 leads for SaaS products")

    assert result is not None
    assert "leads" in result.lower()
    assert len(result) > 100  # Substantive response
```

### Integration Tests (20% of tests)

```python
# tests/integration/test_multi_agent_workflow.py
import pytest
from app.agent import agent as root_agent

@pytest.mark.asyncio
async def test_end_to_end_sales_workflow():
    """Test complete workflow from lead gen to proposal."""
    result = await root_agent.run(
        "Find 5 leads for our AI platform, then create a proposal for the top lead"
    )

    # Verify multi-agent coordination
    assert "leads" in result.lower()
    assert "proposal" in result.lower()
```

### Vertex AI Evaluation

```python
# evaluations/run_evaluation.py
from vertexai.preview.evaluation import EvalTask

eval_dataset = [
    {
        "prompt": "Find CTOs at fintech companies",
        "reference": "Should return LinkedIn profiles with titles and companies"
    },
    # ... more examples
]

eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=["bleu", "rouge", "fluency", "coherence"],
    experiment="sales-agent-v1"
)

result = eval_task.evaluate(
    model=sales_agent,
    experiment_run_name="run-2025-01-15"
)
```

### Load Testing

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class AgentUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def query_agent(self):
        self.client.post("/query", json={
            "message": "Test query",
            "session_id": f"test-session-{self.environment.runner.user_count}"
        })
```

**Run:** `locust -f tests/load/locustfile.py --host https://your-agent.run.app`

---

## 4. Infrastructure as Code Patterns

### Multi-Environment Pattern

Use **`for_each`** to deploy staging and prod from same code:

```hcl
# deployment/terraform/locals.tf
locals {
  deploy_project_ids = toset(compact([
    var.staging_project_id != "" ? var.staging_project_id : null,
    var.prod_project_id != "" ? var.prod_project_id : null
  ]))

  # Map project to environment
  project_to_env = {
    for pid in local.deploy_project_ids :
    pid => pid == var.prod_project_id ? "prod" : "staging"
  }
}

# deployment/terraform/cloud_run.tf
resource "google_cloud_run_v2_service" "agent" {
  for_each = local.deploy_project_ids

  project  = each.key
  name     = "${var.project_name}-agent"
  location = var.region

  template {
    scaling {
      min_instance_count = local.project_to_env[each.key] == "prod" ? 1 : 0
      max_instance_count = local.project_to_env[each.key] == "prod" ? 100 : 10
    }

    service_account = google_service_account.app[each.key].email
  }
}
```

### Service Account Hierarchy

```hcl
# deployment/terraform/service_accounts.tf

# 1. CI/CD Service Account - Builds and deploys
resource "google_service_account" "cicd" {
  project      = var.dev_project_id
  account_id   = "${var.project_name}-cicd"
  display_name = "CI/CD Pipeline SA"
}

resource "google_project_iam_member" "cicd_roles" {
  for_each = toset([
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin",
    "roles/artifactregistry.writer"
  ])

  project = var.dev_project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.cicd.email}"
}

# 2. Application Runtime Service Account - Agent execution
resource "google_service_account" "app" {
  for_each = local.deploy_project_ids

  project      = each.key
  account_id   = "${var.project_name}-app"
  display_name = "Agent Runtime SA"
}

resource "google_project_iam_member" "app_roles" {
  for_each = {
    for pair in setproduct(local.deploy_project_ids, [
      "roles/aiplatform.user",
      "roles/logging.logWriter",
      "roles/cloudtrace.agent",
      "roles/storage.objectCreator"
    ]) : "${pair[0]}-${pair[1]}" => {
      project = pair[0]
      role    = pair[1]
    }
  }

  project = each.value.project
  role    = each.value.role
  member  = "serviceAccount:${google_service_account.app[each.value.project].email}"
}
```

### BigQuery Log Sinks

```hcl
# deployment/terraform/log_sinks.tf
resource "google_bigquery_dataset" "telemetry" {
  for_each = local.deploy_project_ids

  project    = each.key
  dataset_id = "agent_telemetry"
  location   = var.region

  default_partition_expiration_ms = 7776000000  # 90 days
}

resource "google_logging_project_sink" "telemetry" {
  for_each = local.deploy_project_ids

  project     = each.key
  name        = "agent-telemetry-sink"
  destination = "bigquery.googleapis.com/projects/${each.key}/datasets/${google_bigquery_dataset.telemetry[each.key].dataset_id}"

  filter = <<-EOT
    resource.type="cloud_run_revision"
    jsonPayload.event_type="span"
  EOT

  bigquery_options {
    use_partitioned_tables = true
  }
}
```

---

## 5. CI/CD Best Practices

### GitHub Actions Workflow Pattern

```yaml
# .github/workflows/pr.yaml
name: PR Validation
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync

      - name: Run linters
        run: |
          uv run ruff check app/ tests/
          uv run mypy app/

      - name: Run tests
        run: uv run pytest tests/ -v --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

```yaml
# .github/workflows/deploy-staging.yaml
name: Deploy to Staging
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.CICD_SA_EMAIL }}

      - name: Build and push image
        run: |
          gcloud builds submit \
            --tag ${{ secrets.REGION }}-docker.pkg.dev/${{ secrets.STAGING_PROJECT }}/agents/agent:${{ github.sha }}

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy agent \
            --image ${{ secrets.REGION }}-docker.pkg.dev/${{ secrets.STAGING_PROJECT }}/agents/agent:${{ github.sha }} \
            --project ${{ secrets.STAGING_PROJECT }} \
            --region ${{ secrets.REGION }} \
            --service-account ${{ secrets.APP_SA_EMAIL }}

      - name: Run smoke tests
        run: uv run pytest tests/e2e/ --env staging
```

```yaml
# .github/workflows/deploy-prod.yaml
name: Deploy to Production
on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    environment:
      name: production
      url: https://agent.example.com

    steps:
      # Same as staging but:
      # 1. Promote image from staging (don't rebuild)
      # 2. Requires manual approval (environment protection)
      # 3. Deploy with prod config

      - name: Promote image
        run: |
          docker pull ${{ secrets.REGION }}-docker.pkg.dev/${{ secrets.STAGING_PROJECT }}/agents/agent:${{ github.sha }}
          docker tag ... ${{ secrets.REGION }}-docker.pkg.dev/${{ secrets.PROD_PROJECT }}/agents/agent:${{ github.ref_name }}
          docker push ...
```

### Deployment Strategy

1. **PR → Staging → Production Flow**
   - Every PR: Automated tests + lint
   - Merge to `main`: Auto-deploy to staging
   - Create tag `v1.0.0`: Manual approval → prod deployment

2. **Image Promotion**
   - Build once in staging
   - Promote same image to production
   - Never build different images for prod

3. **Rollback Strategy**
   - Cloud Run: Instant rollback to previous revision
   - Agent Engine: Redeploy previous versioned agent

---

## 6. Security and Compliance Requirements

### Least Privilege IAM

**Principle:** Grant minimum permissions required for each service account.

```hcl
# CI/CD SA: Can deploy but cannot access production data
roles/run.admin                    # Deploy Cloud Run
roles/iam.serviceAccountUser       # Impersonate app SA
roles/artifactregistry.writer      # Push images

# App SA: Can execute agent logic but cannot modify infrastructure
roles/aiplatform.user              # Call Vertex AI
roles/logging.logWriter            # Write logs
roles/cloudtrace.agent             # Write traces
roles/storage.objectCreator        # Store large trace payloads
```

### PII and Sensitive Data Handling

**In Logging:**

```python
# app/app_utils/tracing.py
import re

def mask_pii(text: str) -> str:
    """Mask PII before logging."""
    # Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***EMAIL***', text)
    # Phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '***PHONE***', text)
    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***SSN***', text)
    # Credit card
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '***CC***', text)
    return text

# Use in span attributes
span.set_attribute("user_query", mask_pii(query))
```

**In BigQuery:**

```sql
-- Create view with PII redacted
CREATE VIEW agent_telemetry.spans_safe AS
SELECT
  trace_id,
  span_id,
  REGEXP_REPLACE(span_name, r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***') AS span_name,
  -- Redact email from all string fields
FROM agent_telemetry.spans_raw;
```

### Secret Management

```python
# app/app_utils/secrets.py
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version: str = "latest") -> str:
    """Fetch secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
api_key = get_secret(PROJECT_ID, "third-party-api-key")
```

---

## 7. Multi-Agent System Design Principles

### Hierarchical Architecture

```
Level 0: Root Orchestrator
  ├─ Level 1: Division Coordinators (functional areas)
  │   ├─ Level 2: Team Agents (specialized teams)
  │   │   └─ Level 3: Specialist Agents (leaf tasks)
```

**Design Principles:**

1. **Single Responsibility**: Each agent has ONE clear purpose
2. **Clear Descriptions**: LLM uses descriptions for routing - make them specific
3. **Delegation Over Duplication**: Don't duplicate capabilities - delegate to specialist
4. **Bounded Context**: Each agent has limited knowledge domain

### Example: Sales Division

```python
# app/agents/coordinators/sales_division.py
from google_adk.agents import LlmAgent
from app.agents.teams.sales import (
    lead_generation_team,
    deal_closing_team,
    account_management_team
)

sales_division = LlmAgent(
    name="SalesDivision",
    model="gemini-2.0-flash-exp",
    description=(
        "Handles ALL sales-related operations including lead generation, "
        "deal closing, and account management. Route here for prospecting, "
        "proposals, pricing, contract negotiation, and customer retention."
    ),
    sub_agents=[
        lead_generation_team,
        deal_closing_team,
        account_management_team
    ],
    instruction="""You coordinate sales operations across the organization.

ROUTING LOGIC:
- lead_generation_team: Prospecting, lead qualification, cold outreach, LinkedIn, data enrichment
- deal_closing_team: Proposals, pricing, negotiations, contracts, objection handling
- account_management_team: Upsells, retention, customer success, relationship building

IMPORTANT:
1. Choose the MOST SPECIFIC team for each request
2. If a request spans multiple teams, break it into subtasks and route appropriately
3. Synthesize results from multiple teams when needed
4. Maintain context across team boundaries
"""
)
```

### Agent Communication Patterns

**1. Sequential Delegation:**
```python
# User: "Find 5 leads and create a proposal for the best one"
# Flow: Root → Sales Division → Lead Gen Team → Deal Closing Team
```

**2. Parallel Execution:**
```python
# User: "Find leads AND create marketing content"
# Flow: Root → [Sales Division || Marketing Division] → merge results
```

**3. Iterative Refinement:**
```python
# User: "Create a proposal, review it, and revise based on feedback"
# Flow: Deal Closing → Proposal Review Agent → Deal Closing (revision)
```

---

## 8. Observability and Monitoring

### OpenTelemetry Instrumentation

**For ADK Agents:**

```python
# app/agent.py
import os
from google.adk.agents import LlmAgent
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from app.app_utils.tracing import CloudTraceLoggingSpanExporter

# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add custom exporter
span_processor = BatchSpanProcessor(CloudTraceLoggingSpanExporter(
    project_id=os.environ["PROJECT_ID"]
))
trace.get_tracer_provider().add_span_processor(span_processor)

# Agent automatically inherits tracing
agent = LlmAgent(
    name="RootOrchestrator",
    model="gemini-2.0-flash-exp",
    # ... config
)
```

**For LangChain/CrewAI:**

```python
from traceloop.sdk import Traceloop

Traceloop.init(
    app_name="my-agent",
    api_endpoint="https://cloudtrace.googleapis.com/v2/projects/PROJECT_ID/traces",
    disable_batch=False
)
```

### Custom Trace Exporter (256KB Limit Handling)

```python
# app/app_utils/tracing.py
from opentelemetry.sdk.trace.export import SpanExporter
from google.cloud import storage, logging
import json

class CloudTraceLoggingSpanExporter(SpanExporter):
    """Custom exporter that handles large span attributes (>256KB)."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.gcs_client = storage.Client(project=project_id)
        self.bucket = self.gcs_client.bucket(f"{project_id}-trace-payloads")
        self.logging_client = logging.Client(project=project_id)
        self.logger = self.logging_client.logger("agent-traces")

    def export(self, spans):
        for span in spans:
            span_dict = span.to_json()

            # Check size
            if len(json.dumps(span_dict)) > 250_000:  # 250KB threshold
                # Store large payload in GCS
                blob_name = f"traces/{span.context.trace_id}/{span.context.span_id}.json"
                blob = self.bucket.blob(blob_name)
                blob.upload_from_string(json.dumps(span_dict))

                # Log reference with truncated attributes
                self.logger.log_struct({
                    "event_type": "span",
                    "trace_id": span.context.trace_id,
                    "span_id": span.context.span_id,
                    "large_payload_gcs": f"gs://{self.bucket.name}/{blob_name}",
                    "attributes_truncated": True
                })
            else:
                # Normal logging
                self.logger.log_struct({
                    "event_type": "span",
                    **span_dict
                })
```

### BigQuery Analytics Queries

```sql
-- Agent performance by type
SELECT
  JSON_EXTRACT_SCALAR(attributes, '$.agent_name') AS agent_name,
  COUNT(*) AS invocation_count,
  AVG(TIMESTAMP_DIFF(end_time, start_time, MILLISECOND)) AS avg_latency_ms,
  COUNTIF(JSON_EXTRACT_SCALAR(attributes, '$.error') IS NOT NULL) AS error_count
FROM `project.agent_telemetry.spans`
WHERE DATE(start_time) = CURRENT_DATE()
GROUP BY agent_name
ORDER BY invocation_count DESC;

-- Cost analysis
SELECT
  DATE(start_time) AS date,
  JSON_EXTRACT_SCALAR(attributes, '$.model') AS model,
  SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.input_tokens') AS INT64)) AS total_input_tokens,
  SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.output_tokens') AS INT64)) AS total_output_tokens,
  -- Gemini pricing: $0.00025/1K input, $0.00075/1K output
  SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.input_tokens') AS INT64)) * 0.00025 / 1000 +
  SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.output_tokens') AS INT64)) * 0.00075 / 1000 AS estimated_cost_usd
FROM `project.agent_telemetry.spans`
WHERE DATE(start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY date, model
ORDER BY date DESC;
```

### Monitoring Alerts

```hcl
# deployment/terraform/monitoring.tf
resource "google_monitoring_alert_policy" "high_error_rate" {
  display_name = "Agent - High Error Rate"
  combiner     = "OR"

  conditions {
    display_name = "Error rate > 5%"

    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND metric.type=\"run.googleapis.com/request_count\""
      duration        = "300s"
      comparison      = "COMPARISON_GT"
      threshold_value = 0.05

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}
```

---

## 9. Production Readiness Checklist

### Pre-Deployment

- [ ] **Code Quality**
  - [ ] All tests passing (unit, integration, load)
  - [ ] Code coverage > 80%
  - [ ] Linters passing (ruff, mypy)
  - [ ] No hardcoded secrets or credentials

- [ ] **Infrastructure**
  - [ ] Terraform plan reviewed and approved
  - [ ] Service accounts created with least privilege
  - [ ] IAM roles assigned correctly
  - [ ] Secrets stored in Secret Manager
  - [ ] BigQuery datasets created
  - [ ] Log sinks configured

- [ ] **Observability**
  - [ ] OpenTelemetry instrumentation verified in dev
  - [ ] Traces visible in Cloud Trace
  - [ ] Logs flowing to Cloud Logging
  - [ ] BigQuery receiving telemetry data
  - [ ] Dashboards created and tested
  - [ ] Alerts configured and tested

- [ ] **CI/CD**
  - [ ] GitHub Actions workflows configured
  - [ ] Workload Identity Federation setup
  - [ ] Staging environment deployed and tested
  - [ ] Promotion workflow tested
  - [ ] Rollback procedure documented

- [ ] **Security**
  - [ ] Service account keys NOT used (WIF instead)
  - [ ] PII masking implemented
  - [ ] Secrets rotated within last 90 days
  - [ ] IAM audit passed
  - [ ] VPC-SC configured (if required)

- [ ] **Performance**
  - [ ] Load testing completed
  - [ ] P99 latency < SLO
  - [ ] Auto-scaling tested
  - [ ] Cost projection reviewed

### Post-Deployment

- [ ] **Validation**
  - [ ] Smoke tests passed
  - [ ] End-to-end workflow verified
  - [ ] Traces visible in Cloud Trace
  - [ ] Dashboards populating with data
  - [ ] No errors in last 1 hour

- [ ] **Monitoring**
  - [ ] Error rate < 1%
  - [ ] P99 latency within SLO
  - [ ] Cost within budget
  - [ ] Alerts functioning correctly

- [ ] **Documentation**
  - [ ] README updated with deployment info
  - [ ] Runbooks created
  - [ ] Architecture diagrams current
  - [ ] Handoff docs complete

### Ongoing Operations

- [ ] **Weekly**
  - [ ] Review error rates and trends
  - [ ] Check cost anomalies
  - [ ] Review agent performance metrics
  - [ ] Triage new issues

- [ ] **Monthly**
  - [ ] Rotate secrets
  - [ ] Update dependencies
  - [ ] Review and optimize high-cost agents
  - [ ] Audit IAM permissions

- [ ] **Quarterly**
  - [ ] Conduct load testing
  - [ ] Review and update runbooks
  - [ ] Security audit
  - [ ] Architecture review

---

## Summary

These best practices synthesize patterns from the Agent Starter Pack and ensure:

1. **Consistency**: Standard structure across all projects
2. **Reliability**: Comprehensive testing and monitoring
3. **Security**: Least privilege, secret management, PII protection
4. **Scalability**: Infrastructure as code, auto-scaling, cost optimization
5. **Maintainability**: Clear documentation, operational runbooks
6. **Observability**: Full instrumentation, analytics, alerting

Following these practices will result in **production-ready, enterprise-grade agent systems** that are secure, performant, and maintainable.

---

**Next Steps:**
1. Apply these patterns to your specific agent project
2. Customize for your organization's requirements
3. Iterate based on production learnings
4. Share improvements back with the team
