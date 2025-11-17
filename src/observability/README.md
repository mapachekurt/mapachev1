# Observability Layer

Comprehensive observability implementation for agent systems with structured logging, distributed tracing, metrics collection, and dashboard definitions.

## Overview

The observability layer provides four core components:

1. **Structured Logging** (`structured_logging.py`) - JSON-formatted logs with automatic context injection
2. **Distributed Tracing** (`distributed_tracing.py`) - OpenTelemetry-based distributed tracing
3. **Metrics Collection** (`metrics.py`) - Prometheus-compatible metrics
4. **Dashboard Definitions** (`dashboards.py`) - Pre-configured monitoring dashboards

## Features

- **Works without cloud resources** - All components use mocks/stubs when dependencies are unavailable
- **Full type hints** - Complete type annotations throughout
- **Production-ready** - Comprehensive error handling and graceful degradation
- **Framework-agnostic** - Can be integrated with any Python application

## Installation

Optional dependencies (components work without these):

```bash
pip install structlog  # For structured logging
pip install opentelemetry-api opentelemetry-sdk  # For distributed tracing
pip install prometheus-client  # For metrics
```

## Quick Start

```python
from observability import get_logger, get_tracer, get_metrics

# Initialize components
logger = get_logger(agent_id="agent-001", environment="production")
tracer = get_tracer(service_name="agent-service")
metrics = get_metrics(namespace="agent", subsystem="workflow")

# Use in your agent code
logger.info("Processing task", task_id="task-123", priority="high")

with tracer.start_span("process_task", task_id="task-123") as span:
    with metrics.track_request(agent_id="agent-001", task_type="processing"):
        # Your task logic here
        span.set_attribute("status", "processing")
        result = process_data()

        # Record metrics
        metrics.record_cost(agent_id="agent-001", cost_usd=0.05, cost_type="llm")
```

## Components

### 1. Structured Logging

```python
from observability import get_logger

logger = get_logger(agent_id="agent-001")

# Basic logging
logger.info("Task started", task_id="task-123")
logger.error("Task failed", task_id="task-123", error="Timeout")

# Context binding
logger.bind(session_id="session-456")
logger.info("Processing")  # Includes session_id automatically

# Specialized logging
logger.log_task_start("task-123", "data_processing", priority="high")
logger.log_task_end("task-123", "data_processing", success=True, duration_ms=1234.5)
logger.log_agent_action("data_validated", records=100)
```

### 2. Distributed Tracing

```python
from observability import get_tracer

tracer = get_tracer(service_name="agent-service")

# Start a span
with tracer.start_span("process_data", task_id="task-123") as span:
    span.set_attribute("records", 100)
    process_data()

# Trace LLM calls
with tracer.trace_llm_call("gpt-4", "openai", prompt_tokens=150) as span:
    response = call_llm()
    span.set_attribute("completion_tokens", 75)

# Context propagation
context = tracer.inject_context()
# Send context to child service...

# In child service:
with tracer.start_span_with_context("child_task", context):
    # Work is traced as part of parent context
    process_child_task()
```

### 3. Metrics Collection

```python
from observability import get_metrics

metrics = get_metrics(namespace="agent")

# Track requests automatically
with metrics.track_request(agent_id="agent-001", task_type="processing"):
    process_task()  # Duration, active requests, success/failure tracked

# Record specific metrics
metrics.record_cost(agent_id="agent-001", cost_usd=0.05, cost_type="llm")
metrics.record_llm_tokens("agent-001", "gpt-4", prompt_tokens=150, completion_tokens=75)
metrics.record_error("agent-001", "TimeoutError")
metrics.set_queue_depth("agent-001", "tasks", 42)
metrics.set_memory_usage("agent-001", 512 * 1024 * 1024)  # 512 MB

# Export metrics for Prometheus
metrics_output = metrics.get_metrics_output()
# Serve at /metrics endpoint
```

### 4. Dashboard Definitions

```python
from observability import get_dashboard, get_all_dashboards

# Get pre-defined dashboards
overview = get_dashboard("overview")
performance = get_dashboard("performance")
llm_metrics = get_dashboard("llm_metrics")
error_analysis = get_dashboard("error_analysis")

# Export to JSON
json_config = overview.to_json()

# Get all dashboards
dashboards = get_all_dashboards()
for name, dashboard in dashboards.items():
    print(f"{name}: {dashboard.description}")
```

## Metrics Reference

### Counters
- `agent_system_requests_total` - Total requests by agent, task type, and status
- `agent_system_cost_usd_total` - Accumulated costs by agent and cost type
- `agent_system_errors_total` - Total errors by agent and error type
- `agent_system_llm_tokens_total` - LLM tokens by agent, model, and token type

### Histograms
- `agent_system_duration_seconds` - Request duration distribution
- `agent_system_task_duration_seconds` - Task duration distribution

### Gauges
- `agent_system_active_requests` - Currently active requests
- `agent_system_queue_depth` - Queue depth by agent and queue name
- `agent_system_memory_usage_bytes` - Memory usage by agent

## Dashboard Types

1. **Agent System Overview** - High-level health and performance metrics
2. **Agent Performance Metrics** - Detailed performance analysis
3. **LLM Metrics & Costs** - Token usage and cost tracking
4. **Error Analysis** - Error tracking and debugging

## Example Usage

See `example_usage.py` for comprehensive examples including:
- Single task simulation with full observability
- Agent fleet simulation with multiple agents
- Dashboard configuration export
- Distributed tracing context propagation

Run the example:
```bash
python -m observability.example_usage
```

## Architecture

```
observability/
├── __init__.py              # Public API exports
├── structured_logging.py    # AgentLogger class
├── distributed_tracing.py   # AgentTracer class
├── metrics.py               # AgentMetrics class
├── dashboards.py            # Dashboard definitions
├── example_usage.py         # Usage examples
└── README.md               # This file
```

## Best Practices

1. **Initialize once** - Create logger/tracer/metrics instances once and reuse
2. **Use context managers** - Leverage `with` statements for automatic cleanup
3. **Add context** - Include task_id, agent_id, and relevant metadata in logs/spans
4. **Track costs** - Record LLM token usage and costs for budget monitoring
5. **Set up dashboards** - Import dashboard configs into your monitoring platform
6. **Monitor errors** - Track error rates and types for proactive debugging

## Integration with Monitoring Platforms

### Prometheus
```python
from prometheus_client import start_http_server
from observability import get_metrics

metrics = get_metrics()
start_http_server(8000)  # Metrics available at http://localhost:8000/metrics
```

### Grafana
```python
from observability import create_grafana_config
import json

config = create_grafana_config()
with open("grafana_dashboards.json", "w") as f:
    json.dump(config, f, indent=2)
# Import grafana_dashboards.json into Grafana
```

### Looker Studio
```python
from observability import create_looker_studio_config
import json

config = create_looker_studio_config()
with open("looker_config.json", "w") as f:
    json.dump(config, f, indent=2)
# Import into Looker Studio
```

## Troubleshooting

**Q: Components not working?**
A: All components gracefully degrade when optional dependencies are missing. Check logs for warnings.

**Q: No metrics appearing?**
A: Ensure Prometheus client is installed and metrics endpoint is exposed.

**Q: Traces not showing?**
A: Verify OpenTelemetry SDK is installed and exporter is configured.

**Q: Logs not structured?**
A: Install structlog for JSON formatting. Falls back to standard logging otherwise.

## License

Part of the Mapache v1 Agent Framework.
