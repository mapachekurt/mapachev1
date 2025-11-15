# Agent Starter Pack - Complete Observability Patterns Analysis

## Overview

The Agent Starter Pack implements a comprehensive observability architecture using Google Cloud Platform services, OpenTelemetry instrumentation, and custom exporters. This document provides a detailed analysis of all observability patterns and best practices.

---

## 1. OpenTelemetry Instrumentation Implementation

### 1.1 Core Architecture

The Agent Starter Pack uses OpenTelemetry as the foundational observability framework, providing:

- **Automatic instrumentation** of LangChain and CrewAI operations
- **Span-based tracing** with Google Cloud Trace integration
- **Structured logging** with Google Cloud Logging
- **Batch processing** for efficient span export

### 1.2 Tracer Provider Setup

#### For LangChain/CrewAI Agents (Non-ADK)
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from traceloop.sdk import Instruments, Traceloop
from app_utils.tracing import CloudTraceLoggingSpanExporter

# Initialize Traceloop SDK with custom exporter
Traceloop.init(
    app_name="my-agent",
    disable_batch=False,
    exporter=CloudTraceLoggingSpanExporter(),
    instruments={Instruments.LANGCHAIN, Instruments.CREW},
)
```

**Key Points:**
- `disable_batch=False` ensures spans are batched for performance
- Instruments both LANGCHAIN and CREW libraries automatically
- Traceloop SDK wraps OpenTelemetry for convenience

#### For ADK Agents

```python
import google.auth
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from app_utils.tracing import CloudTraceLoggingSpanExporter

_, project_id = google.auth.default()
provider = TracerProvider()
processor = export.BatchSpanProcessor(
    CloudTraceLoggingSpanExporter(project_id=project_id)
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

**Benefits:**
- Direct OpenTelemetry API usage for fine-grained control
- Automatic project ID detection from environment
- BatchSpanProcessor batches spans before export

### 1.3 Instrumentation Scope

The framework automatically instruments:

1. **LangChain Components:**
   - LLM calls
   - Chain execution
   - Tool invocations
   - Memory operations
   - Retrieval operations

2. **CrewAI Components:**
   - Agent execution flows
   - Task execution
   - Tool usage
   - Inter-agent communication

3. **Custom Tracing:**
   - Span association properties for correlation
   - Metadata enrichment (user_id, session_id, commit_sha)
   - Request-scoped context propagation

### 1.4 Tracing Association Properties

```python
def set_tracing_properties(config: RunnableConfig) -> None:
    """Sets tracing association properties for the current request."""
    Traceloop.set_association_properties(
        {
            "log_type": "tracing",
            "run_id": str(config.get("run_id", "None")),
            "user_id": config["metadata"].pop("user_id", "None"),
            "session_id": config["metadata"].pop("session_id", "None"),
            "commit_sha": os.environ.get("COMMIT_SHA", "None"),
        }
    )
```

**Properties Added:**
- `log_type`: "tracing" for filtering in BigQuery
- `run_id`: Unique identifier for the request execution
- `user_id`: Application-level user identifier
- `session_id`: Conversation/session context
- `commit_sha`: Git commit SHA for version tracking

---

## 2. Custom CloudTraceSpanExporter Implementation

### 2.1 CloudTraceLoggingSpanExporter Class

Located in: `app_utils/tracing.py`

```python
from google.cloud import logging as google_cloud_logging
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import ReadableSpan

class CloudTraceLoggingSpanExporter(CloudTraceSpanExporter):
    """
    An extended version of CloudTraceSpanExporter that logs span data to 
    Google Cloud Logging and handles large attribute values by storing them 
    in Google Cloud Storage.
    """

    def __init__(
        self,
        logging_client: google_cloud_logging.Client | None = None,
        storage_client: storage.Client | None = None,
        bucket_name: str | None = None,
        debug: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.debug = debug
        self.logging_client = logging_client or google_cloud_logging.Client(
            project=self.project_id
        )
        self.logger = self.logging_client.logger(__name__)
        self.storage_client = storage_client or storage.Client(
            project=self.project_id
        )
        self.bucket_name = bucket_name or f"{self.project_id}-logs"
        self.bucket = self.storage_client.bucket(self.bucket_name)
```

### 2.2 Purpose and Design

**Why Custom Exporter?**

The standard CloudTraceSpanExporter has limitations:
- Cloud Trace has a **256-byte limit** on individual attribute values
- Cloud Logging has a **256KB limit** on log entries
- Large LLM outputs (prompts, completions) exceed these limits

**Solution:**
The custom exporter works around these limitations by:

1. **Exporting to Cloud Trace**: Uses parent class method for standard trace export
2. **Exporting to Cloud Logging**: Creates structured log entries with span data
3. **Large Payload Handling**: Stores oversized attributes in GCS and creates references

### 2.3 Export Process

```python
def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
    """Export the spans to Google Cloud Logging and Cloud Trace."""
    for span in spans:
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, "x")
        span_id = format(span_context.span_id, "x")
        span_dict = json.loads(span.to_json())

        # Add trace and span IDs for Cloud Logging
        span_dict["trace"] = f"projects/{self.project_id}/traces/{trace_id}"
        span_dict["span_id"] = span_id

        # Process large attributes
        span_dict = self._process_large_attributes(
            span_dict=span_dict, span_id=span_id
        )

        if self.debug:
            print(span_dict)

        # Log to Cloud Logging
        self.logger.log_struct(
            span_dict,
            labels={
                "type": "agent_telemetry",
                "service_name": "my-agent",
            },
            severity="INFO",
        )
    
    # Also export to Cloud Trace
    return super().export(spans)
```

**Flow:**
1. Extract trace and span IDs
2. Convert span to JSON dictionary
3. Process large attributes (delegate to GCS if needed)
4. Log structured entry to Cloud Logging
5. Export to Cloud Trace via parent class

### 2.4 Large Attribute Processing

```python
def _process_large_attributes(self, span_dict: dict, span_id: str) -> dict:
    """
    Process large attribute values by storing them in GCS if they exceed 
    the size limit of Google Cloud Logging.
    """
    attributes = span_dict["attributes"]
    
    # Check if total attributes exceed 250KB threshold
    if len(json.dumps(attributes).encode()) > 255 * 1024:  # 250 KB
        attributes_payload = dict(attributes.items())
        attributes_retain = dict(attributes.items())

        # Store large payload in GCS
        gcs_uri = self.store_in_gcs(
            json.dumps(attributes_payload), 
            span_id
        )
        
        # Keep references instead of full payload
        attributes_retain["uri_payload"] = gcs_uri
        attributes_retain["url_payload"] = (
            f"https://storage.mtls.cloud.google.com/"
            f"{self.bucket_name}/spans/{span_id}.json"
        )

        span_dict["attributes"] = attributes_retain
        logging.info(
            "Length of payload span above 250 KB, storing attributes in GCS "
            "to avoid large log entry errors"
        )

    return span_dict
```

### 2.5 GCS Storage for Large Payloads

```python
def store_in_gcs(self, content: str, span_id: str) -> str:
    """
    Store large content in Google Cloud Storage.
    
    Args:
        content: The JSON content to store
        span_id: The ID of the span for naming
        
    Returns:
        The GCS URI of the stored content
    """
    # Verify bucket exists
    if not self.storage_client.bucket(self.bucket_name).exists():
        logging.warning(
            f"Bucket {self.bucket_name} not found. "
            "Unable to store span attributes in GCS."
        )
        return "GCS bucket not found"

    # Upload to GCS
    blob_name = f"spans/{span_id}.json"
    blob = self.bucket.blob(blob_name)
    blob.upload_from_string(content, "application/json")
    
    return f"gs://{self.bucket_name}/{blob_name}"
```

**Storage Pattern:**
- Path: `gs://{project_id}-logs/spans/{span_id}.json`
- Format: JSON
- Content-Type: `application/json`
- References stored in Cloud Logging for easy lookup

### 2.6 Configuration for ADK Agents

For ADK agents with special labeling:

```python
# In app_utils/tracing.py - Template-aware configuration
self.logger.log_struct(
    span_dict,
    labels={
        "type": "agent_telemetry",
        "service_name": "{{cookiecutter.project_name}}",
    },
    severity="INFO",
)
```

This enables filtering in Cloud Logging and BigQuery based on agent type and service name.

---

## 3. Cloud Trace Integration Details

### 3.1 Cloud Trace API Setup

**Required APIs (enabled via Terraform):**
```terraform
resource "google_project_service" "deploy_project_services" {
  service = "cloudtrace.googleapis.com"
}
```

**Required IAM Roles:**
```terraform
variable "app_sa_roles" {
  default = [
    "roles/cloudtrace.agent",
    "roles/logging.logWriter",
    # ... other roles
  ]
}
```

### 3.2 Trace Hierarchy

**Trace IDs:**
- Generated by OpenTelemetry SDK
- Linked in Cloud Logging entries via `"trace"` field
- Format: `projects/{project_id}/traces/{trace_id}`

**Span Relationships:**
```json
{
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "parent_span_id": "a4a5b12c8e0b8e8a",
  "name": "LLMCall",
  "status": "OK",
  "attributes": {
    "llm.model": "gemini-1.5-pro",
    "llm.prompt_tokens": 250,
    "llm.completion_tokens": 150
  }
}
```

### 3.3 Automatic Trace Linking

Cloud Logging automatically links to Cloud Trace:

1. Log entry contains `trace` field with full trace path
2. Cloud Logging UI shows "Trace" link
3. Click to navigate to Cloud Trace console
4. All spans with same trace_id appear in waterfall view

### 3.4 Quotas and Limits

**Cloud Trace Limitations:**
- 256-byte limit per attribute value
- ~1MB per span total
- ~1000 requests/second per project

**Workarounds in Framework:**
- Large values stored in GCS (>256KB)
- References kept in Cloud Logging
- Span batching in BatchSpanProcessor

---

## 4. Cloud Logging Configuration and Patterns

### 4.1 Logging Client Setup

```python
from google.cloud import logging as google_cloud_logging

logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
```

### 4.2 Structured Logging Patterns

#### Span Logging
```python
self.logger.log_struct(
    span_dict,
    labels={
        "type": "agent_telemetry",
        "service_name": "my-agent",
    },
    severity="INFO",
)
```

#### Setup Message Logging
```python
# For WebSocket setup messages in ADK Live
logger.log_struct(
    {**data["setup"], "type": "setup"}, 
    severity="INFO"
)
```

#### Feedback Logging
```python
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback."""
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}
```

### 4.3 Feedback Schema

```python
class Feedback(BaseModel):
    """Represents feedback for a conversation."""
    score: int | float                          # 1-5 or 0-100
    text: str | None = ""                       # Optional feedback text
    invocation_id: str                          # For ADK agents
    run_id: str                                 # For non-ADK agents
    log_type: Literal["feedback"] = "feedback"  # Used for filtering
    service_name: str                           # Agent name
    user_id: str = ""                           # User identifier
```

### 4.4 Log Levels and Severity

**Used Severity Levels:**
- `INFO`: Normal spans and feedback
- `ERROR`: Error conditions in tracing
- `WARNING`: Issues like missing GCS buckets

**Filtering Examples:**
```
resource.type="cloud_function"
severity="INFO"
jsonPayload.log_type="feedback"

resource.type="cloud_run_revision"
severity="INFO"
labels.type="agent_telemetry"
```

### 4.5 Log Entry Size Limits

**Cloud Logging Quotas:**
- Individual entry size: 256KB (1MB compressed)
- Max 100 entries/second per logger
- Retention: 30 days (default)

**Handling Large Logs:**
```python
# Check size before logging
log_size = len(json.dumps(span_dict).encode())
if log_size > 256 * 1024:  # 256KB
    # Store in GCS and keep reference
    gcs_uri = store_in_gcs(json.dumps(span_dict), span_id)
    span_dict["gcs_reference"] = gcs_uri
```

### 4.6 Log Router Integration

See Section 8 for detailed log routing configuration.

---

## 5. Large Payload Handling (256KB Limit Workarounds)

### 5.1 Problem Statement

**Limits Encountered:**
1. Cloud Trace: 256-byte per attribute value
2. Cloud Logging: 256KB per log entry
3. LLM outputs: Can be much larger (prompts + completions)

### 5.2 Multi-Layer Solution Architecture

```
┌─────────────────────────────────────────────┐
│         OpenTelemetry Spans                 │
│  (LLM outputs, prompts, completions)        │
└──────────────┬──────────────────────────────┘
               │
     ┌─────────┴──────────┬────────────┐
     │                    │            │
     ▼                    ▼            ▼
┌──────────────┐   ┌────────────┐  ┌──────────┐
│ Cloud Trace  │   │   Cloud    │  │   GCS    │
│ (256 bytes)  │   │  Logging   │  │(unlimited)
│              │   │ (256KB)    │  │          │
└──────────────┘   └────────────┘  └──────────┘
```

### 5.3 Span Attribute Size Management

**Phase 1: Attribute Serialization**
```python
span_dict = json.loads(span.to_json())
attributes = span_dict["attributes"]
total_size = len(json.dumps(attributes).encode())
```

**Phase 2: Size Check**
```python
if total_size > 250 * 1024:  # Using 250KB threshold
    # Exceeds limit, need GCS storage
    store_in_gcs_and_reference(attributes)
else:
    # Fits in Cloud Logging, proceed normally
    logger.log_struct(span_dict, severity="INFO")
```

**Phase 3: GCS Storage**
```python
def store_in_gcs(content: str, span_id: str) -> str:
    blob_name = f"spans/{span_id}.json"
    blob = self.bucket.blob(blob_name)
    blob.upload_from_string(content, "application/json")
    return f"gs://{self.bucket_name}/{blob_name}"
```

**Phase 4: Reference Retention**
```python
attributes_retain["uri_payload"] = gcs_uri
attributes_retain["url_payload"] = (
    f"https://storage.mtls.cloud.google.com/"
    f"{bucket_name}/spans/{span_id}.json"
)
```

### 5.4 Retry Logic and Error Handling

```python
def store_in_gcs(self, content: str, span_id: str) -> str:
    # Check bucket existence
    if not self.storage_client.bucket(self.bucket_name).exists():
        logging.warning(
            f"Bucket {self.bucket_name} not found. "
            "Unable to store span attributes in GCS."
        )
        return "GCS bucket not found"
    
    try:
        blob = self.bucket.blob(f"spans/{span_id}.json")
        blob.upload_from_string(content, "application/json")
        return f"gs://{self.bucket_name}/spans/{span_id}.json"
    except Exception as e:
        logging.error(f"Failed to upload to GCS: {e}")
        # Gracefully degrade - keep what we can in Cloud Logging
        return "GCS upload failed"
```

### 5.5 Performance Optimization

**Batch Processing:**
```python
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    CloudTraceLoggingSpanExporter(project_id=project_id)
)
provider.add_span_processor(processor)
```

**BatchSpanProcessor Benefits:**
- Collects spans over time
- Exports in batches (default: 512 spans or 5 seconds)
- Reduces API calls and GCS uploads

---

## 6. GCS Storage for Large Payloads

### 6.1 GCS Bucket Creation

**Terraform Configuration:**
```terraform
resource "google_storage_bucket" "logs_data_bucket" {
  for_each = toset(local.all_project_ids)
  name     = "${each.value}-${var.project_name}-logs"
  location = var.region
  project  = each.value
  
  uniform_bucket_level_access = true
  force_destroy               = true
}
```

**Python Utility:**
```python
def create_bucket_if_not_exists(
    bucket_name: str, 
    project: str, 
    location: str
) -> None:
    """Creates a new bucket if it doesn't already exist."""
    storage_client = storage.Client(project=project)
    
    if bucket_name.startswith("gs://"):
        bucket_name = bucket_name[5:]
    
    try:
        storage_client.get_bucket(bucket_name)
        logging.info(f"Bucket {bucket_name} already exists")
    except exceptions.NotFound:
        bucket = storage_client.create_bucket(
            bucket_name,
            location=location,
            project=project,
        )
        logging.info(f"Created bucket {bucket.name} in {bucket.location}")
```

### 6.2 Bucket Naming Convention

Pattern: `{project_id}-{project_name}-logs`

Example:
- Project ID: `my-agent-dev-123`
- Project Name: `customer-qa-agent`
- Bucket: `my-agent-dev-123-customer-qa-agent-logs`

### 6.3 Span Storage Structure

**Path Convention:**
```
gs://my-agent-dev-123-customer-qa-agent-logs/spans/{span_id}.json
```

**Content Structure:**
```json
{
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "name": "LLMCall",
  "start_time": "2025-01-15T10:30:00Z",
  "end_time": "2025-01-15T10:30:05Z",
  "attributes": {
    "llm.model": "gemini-1.5-pro",
    "llm.input_tokens": 1250,
    "llm.output_tokens": 850,
    "llm.prompt": "Long prompt text...",
    "llm.response": "Long response text..."
  }
}
```

### 6.4 IAM Configuration for GCS Access

**Required Service Account Roles:**
```terraform
variable "app_sa_roles" {
  default = [
    "roles/storage.admin",  # Full access for testing/dev
    "roles/logging.logWriter",
    "roles/cloudtrace.agent",
  ]
}
```

**Minimal Permissions (Production):**
```
roles/storage.objectCreator   # Can write objects only
roles/storage.objectViewer    # Can read objects
```

### 6.5 Bucket Lifecycle Management

**Delete Old Spans (Optional):**
```python
# Could be configured via Terraform lifecycle rules
resource "google_storage_bucket" "logs_data_bucket" {
  lifecycle_rule {
    condition {
      age = 90  # Delete after 90 days
    }
    action {
      type = "Delete"
    }
  }
}
```

### 6.6 Cost Optimization

**Storage Costs:**
- Regional bucket (us-central1): ~$0.023/GB/month
- Typical span: 50-200KB
- 1M spans/day: ~150GB/month = ~$3.45/month

**Optimization Strategies:**
1. Archive to Cloud Archive Storage after 30 days
2. Delete after retention period
3. Use Cloud Logging retention instead (cheaper for queries)
4. Compress JSON before storage

---

## 7. BigQuery Export Configuration

### 7.1 BigQuery Dataset Creation

**Terraform Configuration:**
```terraform
resource "google_bigquery_dataset" "feedback_dataset" {
  for_each      = local.deploy_project_ids
  project       = each.value
  dataset_id    = replace("${var.project_name}_feedback", "-", "_")
  friendly_name = "${var.project_name}_feedback"
  location      = var.region
  depends_on    = [google_project_service.deploy_project_services]
}

resource "google_bigquery_dataset" "telemetry_logs_dataset" {
  for_each      = local.deploy_project_ids
  project       = each.value
  dataset_id    = replace("${var.project_name}_telemetry", "-", "_")
  friendly_name = "${var.project_name}_telemetry"
  location      = var.region
  depends_on    = [google_project_service.deploy_project_services]
}
```

**Dataset Configuration:**
- Two datasets per environment (dev, staging, prod)
- Naming: `{project_name}_feedback` and `{project_name}_telemetry`
- Hyphens replaced with underscores (BigQuery naming requirement)
- Location matches deployment region

### 7.2 Log Sinks to BigQuery

**Terraform Configuration:**
```terraform
resource "google_logging_project_sink" "log_export_to_bigquery" {
  for_each = local.deploy_project_ids

  name        = "${var.project_name}_telemetry"
  project     = each.value
  destination = "bigquery.googleapis.com/projects/${each.value}/datasets/${google_bigquery_dataset.telemetry_logs_dataset[each.key].dataset_id}"
  filter      = var.telemetry_logs_filter

  bigquery_options {
    use_partitioned_tables = true  # Critical for performance
  }

  unique_writer_identity = true
  depends_on             = [google_bigquery_dataset.telemetry_logs_dataset]
}

resource "google_logging_project_sink" "feedback_export_to_bigquery" {
  for_each = local.deploy_project_ids

  name        = "${var.project_name}_feedback"
  project     = each.value
  destination = "bigquery.googleapis.com/projects/${each.value}/datasets/${google_bigquery_dataset.feedback_dataset[each.key].dataset_id}"
  filter      = var.feedback_logs_filter

  bigquery_options {
    use_partitioned_tables = true
  }

  unique_writer_identity = true
  depends_on             = [google_bigquery_dataset.feedback_dataset]
}
```

### 7.3 Log Sink Filters

**Telemetry Logs Filter (ADK):**
```
labels.service_name="my-agent" labels.type="agent_telemetry"
```

**Telemetry Logs Filter (LangChain/CrewAI):**
```
jsonPayload.attributes."traceloop.association.properties.log_type"="tracing" 
jsonPayload.resource.attributes."service.name"="my-agent"
```

**Feedback Logs Filter:**
```
jsonPayload.log_type="feedback"
```

### 7.4 Partitioned Tables

**Benefits of Partitioned Tables:**
- Faster queries (only scan relevant partitions)
- Lower costs (reduced data scanned)
- Automatic daily partitions by ingestion time
- Automatic deletion of old partitions

**BigQuery Table Schema (Auto-Generated):**
```
├── timestamp TIMESTAMP (partition key)
├── severity STRING
├── jsonPayload RECORD
│   ├── trace_id STRING
│   ├── span_id STRING
│   ├── name STRING
│   ├── attributes RECORD (JSON)
│   └── status RECORD
├── resource RECORD
│   ├── type STRING
│   └── labels RECORD
├── labels RECORD
│   ├── type STRING (values: "agent_telemetry", "feedback")
│   └── service_name STRING
└── trace STRING (link to Cloud Trace)
```

### 7.5 IAM Permissions for Log Sinks

**Terraform Configuration:**
```terraform
resource "google_project_iam_member" "bigquery_data_editor" {
  for_each = local.deploy_project_ids

  project = each.value
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.log_export_to_bigquery[each.key].writer_identity
}

resource "google_project_iam_member" "feedback_bigquery_data_editor" {
  for_each = local.deploy_project_ids

  project = each.value
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.feedback_export_to_bigquery[each.key].writer_identity
}
```

**Key Points:**
- `unique_writer_identity = true` creates a service account for the sink
- Auto-generated service account gets DataEditor role
- Allows sink to write data to BigQuery

### 7.6 BigQuery Schema Evolution

**Automatic Schema Changes:**
- New attributes in spans automatically added to `jsonPayload.attributes`
- New labels automatically added to `labels` record
- Existing columns never removed (backward compatible)

**Manual Schema Updates:**
```sql
-- Add custom field to existing table
ALTER TABLE `project.dataset.table`
ADD COLUMN custom_field STRING;

-- Update nested field
ALTER TABLE `project.dataset.table`
ADD COLUMN jsonPayload.custom_nested STRING;
```

---

## 8. Log Router Setup

### 8.1 Log Router Architecture

```
Cloud Logging (All Logs)
       │
       ├─────────────┬──────────────┬────────────────┐
       │             │              │                │
       ▼             ▼              ▼                ▼
   Cloud Storage  BigQuery       Cloud Pub/Sub   Cloud Run
   (Archive)      (Analytics)     (Streaming)     (Alerting)
```

### 8.2 Multiple Sinks per Project

**Configuration in Terraform:**

```terraform
locals {
  log_sinks = {
    telemetry = {
      filter      = "labels.type=\"agent_telemetry\""
      destination = "bigquery"
      dataset_id  = google_bigquery_dataset.telemetry_logs_dataset.dataset_id
    }
    feedback = {
      filter      = "jsonPayload.log_type=\"feedback\""
      destination = "bigquery"
      dataset_id  = google_bigquery_dataset.feedback_dataset.dataset_id
    }
    archive = {
      filter      = "severity >= ERROR"
      destination = "gcs"
      bucket_name = google_storage_bucket.error_logs_bucket.name
    }
  }
}

resource "google_logging_project_sink" "router_sinks" {
  for_each = local.log_sinks
  
  name        = each.key
  project     = var.project_id
  destination = "${each.value.destination}.googleapis.com/..."
  filter      = each.value.filter
}
```

### 8.3 Filter Syntax

**Common Filter Patterns:**

```
# Telemetry from specific service
resource.type="cloud_run_revision"
labels.service_name="my-agent"
labels.type="agent_telemetry"

# Feedback from all agents
jsonPayload.log_type="feedback"

# Errors only
severity="ERROR"

# Specific span type
jsonPayload.name="LLMCall"

# Within time range
timestamp >= "2025-01-15T10:00:00Z"
timestamp <= "2025-01-15T11:00:00Z"

# Combined conditions
(labels.service_name="my-agent" OR labels.service_name="other-agent")
AND labels.type="agent_telemetry"
AND severity >= "INFO"
```

### 8.4 Inclusion and Exclusion Filters

**Export all telemetry except debug spans:**
```
labels.type="agent_telemetry"
jsonPayload.severity != "DEBUG"
```

**Export specific time windows:**
```
labels.type="agent_telemetry"
timestamp >= "2025-01-15T00:00:00Z"
timestamp < "2025-01-16T00:00:00Z"
```

### 8.5 Sink Inclusion Filters

**Terraform Sink with Inclusion Filters:**
```terraform
resource "google_logging_project_sink" "telemetry_sink" {
  name = "telemetry-export"
  destination = "bigquery.googleapis.com/projects/..."
  
  filter = "labels.type=\"agent_telemetry\" AND severity >= \"INFO\""
  
  include_children = true  # Include logs from child resources
  
  bigquery_options {
    use_partitioned_tables = true
  }
}
```

### 8.6 Monitoring Sink Health

**Query to check sink status:**
```sql
SELECT
  TIMESTAMP_TRUNC(timestamp, DAY) AS day,
  COUNT(*) AS log_count,
  COUNTIF(jsonPayload.name = "LLMCall") AS llm_calls,
  COUNTIF(jsonPayload.log_type = "feedback") AS feedback_entries
FROM `project.dataset.logs`
GROUP BY day
ORDER BY day DESC
LIMIT 30;
```

---

## 9. Looker Studio Dashboard Patterns

### 9.1 Dashboard Templates

**ADK Agents Dashboard:**
- Link: https://lookerstudio.google.com/c/reporting/46b35167-b38b-4e44-bd37-701ef4307418/page/tEnnC

**LangChain/CrewAI Agents Dashboard:**
- Link: https://lookerstudio.google.com/c/reporting/fa742264-4b4b-4c56-81e6-a667dd0f853f/page/tEnnC

### 9.2 BigQuery Data Source Setup

**Steps in Looker Studio:**

1. Create New Dashboard
2. Add Data Source
3. Select BigQuery
4. Choose Dataset (e.g., `my_agent_telemetry`)
5. Select Table (auto-created by log sink)
6. Click "Connect"

### 9.3 Common Dashboard Visualizations

#### 1. Trace Count Timeline
```sql
SELECT
  TIMESTAMP_TRUNC(timestamp, HOUR) AS hour,
  COUNT(*) AS trace_count,
  COUNT(DISTINCT jsonPayload.trace_id) AS unique_traces
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
GROUP BY hour
ORDER BY hour DESC
```

**Visualization:** Line chart, X=hour, Y=trace_count

#### 2. Error Rate by Service
```sql
SELECT
  labels.service_name,
  COUNTIF(jsonPayload.status.code != 0) AS error_count,
  COUNT(*) AS total_spans,
  ROUND(
    COUNTIF(jsonPayload.status.code != 0) / COUNT(*) * 100, 
    2
  ) AS error_rate_percent
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
GROUP BY labels.service_name
ORDER BY error_rate_percent DESC
```

**Visualization:** Scorecard + Table

#### 3. Feedback Score Distribution
```sql
SELECT
  jsonPayload.score,
  COUNT(*) AS feedback_count,
  ROUND(AVG(jsonPayload.score), 2) AS avg_score
FROM `project.dataset.feedback_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
GROUP BY jsonPayload.score
ORDER BY jsonPayload.score DESC
```

**Visualization:** Bar chart, X=score, Y=feedback_count

#### 4. Response Time Distribution
```sql
SELECT
  jsonPayload.name,
  COUNT(*) AS span_count,
  ROUND(AVG(
    CAST(jsonPayload.end_time AS FLOAT64) - 
    CAST(jsonPayload.start_time AS FLOAT64)
  ) * 1000, 0) AS avg_duration_ms,
  PERCENTILE_CONT(
    CAST(jsonPayload.end_time AS FLOAT64) - 
    CAST(jsonPayload.start_time AS FLOAT64), 
    0.95
  ) * 1000 AS p95_duration_ms
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
GROUP BY jsonPayload.name
ORDER BY avg_duration_ms DESC
```

**Visualization:** Table with custom metrics

#### 5. Token Usage Analysis
```sql
SELECT
  jsonPayload.attributes."llm.model" AS model,
  COUNT(*) AS call_count,
  SUM(CAST(jsonPayload.attributes."llm.input_tokens" AS INT64)) AS total_input_tokens,
  SUM(CAST(jsonPayload.attributes."llm.output_tokens" AS INT64)) AS total_output_tokens,
  ROUND(AVG(CAST(jsonPayload.attributes."llm.input_tokens" AS INT64)), 0) AS avg_input_tokens
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
  AND jsonPayload.name = "LLMCall"
GROUP BY model
ORDER BY call_count DESC
```

**Visualization:** Table

#### 6. User Activity Map
```sql
SELECT
  jsonPayload.attributes."user_id" AS user_id,
  COUNT(*) AS interaction_count,
  COUNT(DISTINCT jsonPayload.attributes."session_id") AS session_count,
  COUNT(DISTINCT DATE(timestamp)) AS days_active,
  ROUND(AVG(
    CAST(jsonPayload.end_time AS FLOAT64) - 
    CAST(jsonPayload.start_time AS FLOAT64)
  ) * 1000, 0) AS avg_duration_ms
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= @start_date AND timestamp <= @end_date
GROUP BY user_id
ORDER BY interaction_count DESC
LIMIT 100
```

**Visualization:** Table

### 9.4 Dashboard Parameters

**Standard Parameters:**
```
@start_date - DATE type (default: 7 days ago)
@end_date   - DATE type (default: today)
@service_name - STRING type (dropdown from table)
@span_type - STRING type (values: "LLMCall", "ToolCall", "ChainCall")
```

### 9.5 Dashboard Refresh Configuration

**Data Freshness:**
- Log sink latency: ~1-2 minutes
- BigQuery table partitions: ~5 minutes
- Looker Studio cache: ~1 hour (configurable)

**Configuration:**
```
Dashboard Settings → Data Freshness
- Auto-refresh: Every 5 minutes
- Email notifications: Daily summary
```

### 9.6 Exporting Dashboard Insights

**Export Options:**
1. **PNG/PDF:** Manual download from dashboard
2. **Scheduled Email:** Daily/weekly reports
3. **Data Studio Pro:** Embed in websites
4. **CSV Export:** Export underlying data

---

## 10. Monitoring and Alerting Setup

### 10.1 Google Cloud Monitoring Integration

**Metrics Published:**
The framework doesn't directly publish metrics, but can be queried via:

1. **Log-based Metrics** (created from logs)
2. **Custom Metrics** (via OpenTelemetry)
3. **BigQuery Analytics** (historical analysis)

### 10.2 Creating Log-based Metrics

**Via Google Cloud Console:**

1. Cloud Logging → Logs Explorer
2. Create a filter
3. "Create Metric" → Log-based Metric
4. Configure metric type, distribution, labels

**Terraform Example:**

```terraform
resource "google_logging_metric" "llm_call_latency" {
  name   = "llm_call_latency_ms"
  filter = "jsonPayload.name=\"LLMCall\""

  metric_descriptor {
    metric_kind = "DISTRIBUTION"
    value_type  = "DISTRIBUTION"
    unit        = "ms"

    labels {
      key         = "model"
      value_type  = "STRING"
      description = "LLM Model"
    }
  }

  value_extractor = "EXTRACT(
    CAST(jsonPayload.end_time AS FLOAT64) - 
    CAST(jsonPayload.start_time AS FLOAT64)
  )"

  label_extractors = {
    "model" = "EXTRACT(jsonPayload.attributes.\"llm.model\")"
  }
}
```

### 10.3 Alert Policies

**High Error Rate Alert:**

```terraform
resource "google_monitoring_alert_policy" "high_error_rate" {
  display_name = "High Error Rate - Agent Telemetry"
  combiner     = "OR"

  conditions {
    display_name = "Error rate > 5%"

    condition_threshold {
      filter = "resource.type=\"cloud_run_revision\" AND metric.type=\"logging.googleapis.com/user/error_rate\""
      
      comparison      = "COMPARISON_GT"
      threshold_value = 5.0
      duration        = "300s"
      
      trigger {
        count = 1
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.slack.id]
}
```

**High Latency Alert:**

```terraform
resource "google_monitoring_alert_policy" "high_latency" {
  display_name = "High LLM Call Latency"
  combiner     = "OR"

  conditions {
    display_name = "P95 latency > 10s"

    condition_threshold {
      filter = "resource.type=\"cloud_run_revision\" AND metric.type=\"logging.googleapis.com/user/llm_call_latency_ms\""
      
      comparison      = "COMPARISON_GT"
      threshold_value = 10000.0  # 10 seconds in ms
      duration        = "600s"
      
      aggregations {
        alignment_period  = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_95"
      }
      
      trigger {
        count = 1
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.email.id]
}
```

**No Data Alert:**

```terraform
resource "google_monitoring_alert_policy" "no_traces" {
  display_name = "No Trace Data Received"
  combiner     = "OR"

  conditions {
    display_name = "No logs in 10 minutes"

    condition_threshold {
      filter = "resource.type=\"cloud_run_revision\" AND labels.type=\"agent_telemetry\""
      
      comparison      = "COMPARISON_LT"
      threshold_value = 1.0
      duration        = "600s"
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
      
      trigger {
        count = 1
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.pagerduty.id]
}
```

### 10.4 Notification Channels

**Types:**
- Email
- Slack
- PagerDuty
- Webhook
- SMS
- Cloud Pub/Sub

**Terraform Example (Slack):**

```terraform
resource "google_monitoring_notification_channel" "slack" {
  display_name = "Agent Observability - Slack"
  type         = "slack"
  
  labels = {
    channel_name = "#agent-alerts"
  }
  
  sensitive_labels {
    auth_token = var.slack_webhook_url
  }
}
```

### 10.5 Dashboard for Monitoring

**Terraform Dashboard:**

```terraform
resource "google_monitoring_dashboard" "agent_observability" {
  dashboard_json = jsonencode({
    displayName = "Agent Observability"
    gridLayout = {
      widgets = [
        {
          title = "Error Rate"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"logging.googleapis.com/user/error_rate\""
                }
              }
            }]
          }
        },
        {
          title = "LLM Call Latency (P95)"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"logging.googleapis.com/user/llm_call_latency_ms\""
                }
              }
            }]
          }
        }
      ]
    }
  })
}
```

### 10.6 Log-based Alerts

**Alert on Specific Span Names:**

```terraform
resource "google_monitoring_alert_policy" "tool_call_errors" {
  display_name = "Tool Call Errors"
  combiner     = "OR"

  conditions {
    display_name = "Tool call with error status"

    condition_threshold {
      filter = "resource.type=\"cloud_run_revision\" AND jsonPayload.name=\"ToolCall\" AND jsonPayload.status.code != 0"
      
      comparison      = "COMPARISON_GT"
      threshold_value = 0.0
      duration        = "60s"
      
      trigger {
        percent = 1.0
      }
    }
  }
}
```

---

## 11. Implementation Best Practices and Patterns

### 11.1 Initialization Pattern

**For Non-ADK (LangChain/CrewAI):**
```python
import logging
from traceloop.sdk import Instruments, Traceloop
from google.cloud import logging as google_cloud_logging
from app_utils.tracing import CloudTraceLoggingSpanExporter

# Setup logging client
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)

# Initialize Traceloop
try:
    Traceloop.init(
        app_name="my-agent",
        disable_batch=False,
        exporter=CloudTraceLoggingSpanExporter(),
        instruments={Instruments.LANGCHAIN, Instruments.CREW},
    )
except Exception as e:
    logging.error(f"Failed to initialize Telemetry: {e}")
    # Continue without tracing rather than failing startup
```

**For ADK:**
```python
import google.auth
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export
from app_utils.tracing import CloudTraceLoggingSpanExporter

_, project_id = google.auth.default()
provider = TracerProvider()
processor = export.BatchSpanProcessor(
    CloudTraceLoggingSpanExporter(project_id=project_id)
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

### 11.2 Configuration Management

**Environment Variables:**
```bash
# Required
export GOOGLE_CLOUD_PROJECT="my-project"

# Optional
export AGENT_VERSION="1.0.0"
export COMMIT_SHA=$(git rev-parse HEAD)
export ALLOW_ORIGINS="https://example.com,https://app.example.com"
```

**Configuration in Code:**
```python
import os

agent_config = {
    "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
    "agent_version": os.environ.get("AGENT_VERSION", "0.1.0"),
    "commit_sha": os.environ.get("COMMIT_SHA", "unknown"),
}
```

### 11.3 Error Handling and Graceful Degradation

**Pattern 1: Try-Except Around Tracing Init**
```python
try:
    Traceloop.init(...)
except Exception as e:
    logging.error(f"Failed to initialize Telemetry: {e}")
    # App continues to work without tracing
```

**Pattern 2: Fallback for Missing GCS Bucket**
```python
try:
    bucket = storage_client.get_bucket(bucket_name)
except exceptions.NotFound:
    logging.warning(f"Bucket {bucket_name} not found")
    # Large payloads won't be stored, but app continues
```

**Pattern 3: Partial Logging on Size Limit**
```python
try:
    if payload_size > 256 * 1024:
        # Store in GCS and keep reference
        gcs_uri = store_in_gcs(payload, span_id)
        payload["gcs_reference"] = gcs_uri
    
    logger.log_struct(payload, severity="INFO")
except Exception as e:
    # Log reduced payload
    reduced_payload = {
        "span_id": span_id,
        "error": str(e),
        "note": "Full payload not logged due to error"
    }
    logger.log_struct(reduced_payload, severity="ERROR")
```

### 11.4 Testing Observability

**Unit Test Pattern:**
```python
def test_tracing_exporter():
    from unittest.mock import Mock, patch
    
    with patch('google.cloud.logging.Client') as mock_logging:
        with patch('google.cloud.storage.Client') as mock_storage:
            exporter = CloudTraceLoggingSpanExporter()
            
            # Verify clients were initialized
            mock_logging.assert_called_once()
            mock_storage.assert_called_once()
            
            # Verify bucket reference
            assert exporter.bucket_name.endswith("-logs")
```

**Integration Test Pattern:**
```python
def test_large_payload_handling():
    from app_utils.tracing import CloudTraceLoggingSpanExporter
    
    exporter = CloudTraceLoggingSpanExporter()
    
    # Create large span
    large_span_dict = {
        "attributes": {
            "llm.prompt": "x" * (300 * 1024),  # 300KB
            "llm.response": "y" * (100 * 1024),  # 100KB
        }
    }
    
    # Should handle gracefully
    result = exporter._process_large_attributes(large_span_dict, "test-span-id")
    
    # Should have GCS references
    assert "uri_payload" in result["attributes"]
    assert "gcs://" in result["attributes"]["uri_payload"]
```

### 11.5 Performance Considerations

**Span Batching:**
- Default batch size: 512 spans
- Default flush interval: 5 seconds
- Memory impact: ~1-2MB for batched spans

**Recommended Configuration for Production:**
```python
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    schedule_delay_millis=1000,  # Flush every second
    max_queue_size=2048,  # Queue up to 2048 spans
    max_export_batch_size=512,  # Export 512 at a time
    export_timeout_millis=30000,  # 30 second timeout
)
```

**High-Load Optimization:**
```python
# Reduce cardinality of spans to export
# Only export spans above certain duration
class FilteringExporter(CloudTraceSpanExporter):
    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        # Filter spans to reduce volume
        filtered_spans = [
            span for span in spans
            if span.end_time - span.start_time > 0.1  # >100ms
        ]
        if filtered_spans:
            return super().export(filtered_spans)
        return SpanExportResult.SUCCESS
```

### 11.6 Security Considerations

**Data Sensitivity:**
- Prompts/completions may contain sensitive data
- Span attributes not encrypted at rest (by default)
- Use labels to segregate PII data

**Access Control:**
```terraform
# Restrict BigQuery access to specific teams
resource "google_bigquery_dataset_iam_member" "telemetry_viewer" {
  dataset_id = google_bigquery_dataset.telemetry_logs_dataset.dataset_id
  role       = "roles/bigquery.dataViewer"
  member     = "group:data-team@example.com"
}

# Restrict GCS bucket access
resource "google_storage_bucket_iam_member" "logs_viewer" {
  bucket = google_storage_bucket.logs_data_bucket.name
  role   = "roles/storage.objectViewer"
  member = "group:support-team@example.com"
}
```

**Field Masking:**
```python
# Custom exporter to mask sensitive fields
def mask_sensitive_fields(span_dict: dict) -> dict:
    attributes = span_dict.get("attributes", {})
    
    # Mask API keys, tokens, etc.
    for key in attributes:
        if any(x in key.lower() for x in ["key", "token", "password", "secret"]):
            attributes[key] = "[REDACTED]"
    
    return span_dict
```

### 11.7 Cost Optimization

**Cloud Trace:**
- Free tier: 2.5 million API units/month
- Excess: $1.00 per million API units
- Strategy: Batch processing, sampling

**Cloud Logging:**
- Free tier: 50GB/month
- Excess: $0.50 per GB ingested
- Strategy: Filter logs at source, use retention policies

**BigQuery:**
- Storage: $0.07/GB/month (multi-region $0.12)
- Queries: $7.50 per TB scanned
- Strategy: Partitioning, clustering, archival

**Cloud Storage:**
- Standard: $0.023/GB/month
- Strategy: Transition to cold storage after 30 days

**Total Estimated Monthly Cost (1M spans/day):**
```
Cloud Trace:       $5-10 (batching helps)
Cloud Logging:     $15-20 (depending on payload size)
BigQuery Storage:  $5-10
BigQuery Queries:  $10-20 (depends on query frequency)
Cloud Storage:     $3-5

Total:             ~$40-65/month
```

---

## 12. Troubleshooting Guide

### 12.1 No Traces Appearing in Cloud Trace

**Checklist:**
1. Verify CloudTraceSpanExporter is initialized
2. Check project_id is correct
3. Verify service account has `roles/cloudtrace.agent`
4. Check Cloud Trace API is enabled
5. Look for initialization errors in logs

**Debug Code:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from app_utils.tracing import CloudTraceLoggingSpanExporter

exporter = CloudTraceLoggingSpanExporter(debug=True)
# Will print span dicts to stdout
```

### 12.2 Large Payloads Not Being Exported

**Checklist:**
1. Verify GCS bucket exists and is accessible
2. Check service account has `roles/storage.admin`
3. Verify bucket name matches configured name
4. Check logs for GCS upload errors

**Test Code:**
```python
import google.cloud.storage as storage

bucket_name = f"{project_id}-my-agent-logs"
storage_client = storage.Client()

try:
    bucket = storage_client.get_bucket(bucket_name)
    print(f"Bucket {bucket_name} exists and is accessible")
except Exception as e:
    print(f"Error accessing bucket: {e}")
```

### 12.3 BigQuery Import Issues

**Common Issues:**

1. **Sink not writing data:**
   - Check sink filter syntax
   - Verify logs match filter
   - Check BigQuery dataset permissions

2. **Data quality issues:**
   - Check timestamp format
   - Verify JSON structure matches schema
   - Look for schema inference errors

**Diagnostic Query:**
```sql
SELECT
  COUNT(*) as total_rows,
  MIN(timestamp) as oldest_timestamp,
  MAX(timestamp) as newest_timestamp,
  COUNT(DISTINCT jsonPayload.trace_id) as unique_traces
FROM `project.dataset.telemetry_logs`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

### 12.4 Feedback Not Being Collected

**Checklist:**
1. Verify `/feedback` endpoint is called with POST
2. Check Feedback model validation
3. Verify Cloud Logging client is initialized
4. Check permissions for BigQuery sink

**Test Code:**
```python
from app_utils.typing import Feedback

feedback = Feedback(
    score=4.5,
    text="Great response",
    run_id="test-run-123",
    log_type="feedback",
    service_name="my-agent",
    user_id="user-123"
)

# Should validate without errors
print(feedback.model_dump_json())
```

---

## 13. Advanced Topics

### 13.1 Custom Span Attributes

**Adding Application-Specific Attributes:**
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("custom.field", "value")
    span.set_attribute("custom.user_id", user_id)
    span.set_attribute("custom.request_id", request_id)
    
    # Business logic here
    result = process_request()
    
    span.set_attribute("custom.result", str(result))
```

### 13.2 Sampling for High-Traffic Services

**Sample only 10% of spans:**
```python
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.sampler import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)

provider = TracerProvider(sampler=sampler)
processor = export.BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
```

### 13.3 Context Propagation

**Propagate trace context across services:**
```python
from opentelemetry.propagators import composite
from opentelemetry.propagators.jaeger import JaegerPropagator

# Use W3C Trace Context + Jaeger propagation
composite.CompositePropagator([
    # The order matters - W3C first
    "tracecontext",
    "jaeger",
])
```

### 13.4 Metrics Export

**Export custom metrics to Cloud Monitoring:**
```python
from opentelemetry.exporter.gcp_monitoring import GoogleCloudMonitoringMetricsExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

metric_exporter = GoogleCloudMonitoringMetricsExporter(project_id=project_id)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
provider = MeterProvider(metric_readers=[metric_reader])

meter = provider.get_meter(__name__)
counter = meter.create_counter("agent.llm.calls")
counter.add(1, {"model": "gemini-1.5-pro"})
```

---

## 14. Complete Deployment Checklist

### Pre-Deployment

- [ ] OpenTelemetry dependencies added to pyproject.toml
- [ ] CloudTraceLoggingSpanExporter copied to app_utils/tracing.py
- [ ] GCS bucket creation function added (app_utils/gcs.py)
- [ ] Feedback model configured in app_utils/typing.py
- [ ] Environment variables configured

### Terraform Deployment

- [ ] APIs enabled (Cloud Trace, Cloud Logging, BigQuery, Cloud Storage)
- [ ] GCS bucket for logs created
- [ ] BigQuery datasets created (telemetry and feedback)
- [ ] Log sinks configured with correct filters
- [ ] IAM roles assigned to service accounts
- [ ] Monitoring alerts configured

### Application Initialization

- [ ] Tracer provider initialized in main app file
- [ ] Batch span processor configured
- [ ] Traceloop initialized (for LangChain/CrewAI)
- [ ] Error handling for initialization failures
- [ ] Logging client initialized

### Verification

- [ ] Send test request to agent
- [ ] Verify spans appear in Cloud Trace (5 min max)
- [ ] Verify logs appear in Cloud Logging (1-2 min)
- [ ] Verify data appears in BigQuery (5 min)
- [ ] Create test Looker Studio dashboard
- [ ] Test feedback collection endpoint

---

## 15. References and Resources

### Official Documentation
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Google Cloud Trace](https://cloud.google.com/trace/docs)
- [Google Cloud Logging](https://cloud.google.com/logging/docs)
- [BigQuery](https://cloud.google.com/bigquery/docs)
- [Looker Studio](https://lookerstudio.google.com/overview)

### Agent Starter Pack Resources
- Repository: https://github.com/GoogleCloudPlatform/agent-starter-pack
- Documentation: https://github.com/GoogleCloudPlatform/agent-starter-pack/docs/guide/observability.md

### Code References
- `app_utils/tracing.py` - CustomCloudTraceLoggingSpanExporter
- `app_utils/gcs.py` - GCS bucket utilities
- `app_utils/typing.py` - Data models (Feedback, etc.)
- `deployment/terraform/log_sinks.tf` - Log routing
- `deployment/terraform/variables.tf` - Configuration

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Framework:** Agent Starter Pack v0.20.4
