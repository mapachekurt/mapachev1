# A2A Protocol Specification

Agent-to-Agent (A2A) communication protocol implementation for opportunity discovery agents.

## Overview

The A2A protocol enables autonomous agents to discover, communicate, and collaborate with each other. This implementation follows the [Linux Foundation A2A standard](https://a2aprotocol.org).

## Protocol Version

Current implementation: **A2A v1.0**

## Core Concepts

### Agent Capabilities

Each agent declares capabilities it can provide:

- **Validation Agent Capabilities:**
  - `pain_point_validation` - Validate problem hypotheses
  - `competitor_analysis` - Analyze competitor weaknesses
  - `evidence_collection` - Collect social media evidence

- **Opportunity Agent Capabilities:**
  - `market_analysis` - Calculate TAM/SAM/SOM
  - `competitive_intelligence` - Map competitive landscape
  - `oss_recommendations` - Find relevant OSS projects
  - `strategic_positioning` - Recommend market position

- **Orchestrator Agent Capabilities:**
  - `agent_orchestration` - Coordinate multiple agents
  - `result_synthesis` - Combine and rank results
  - `project_generation` - Create Linear projects

### Agent Identity

Each agent has:
- **Agent ID**: Unique identifier (e.g., `validation-agent-us-central1`)
- **Endpoint**: URL where agent can be reached
- **Protocol Version**: A2A version supported

## Message Format

### Request Structure

```json
{
  "protocol_version": "1.0",
  "source_agent": {
    "id": "orchestrator-agent",
    "endpoint": "https://example.com/orchestrator"
  },
  "capability": "pain_point_validation",
  "payload": {
    "problem": "construction equipment tracking",
    "subreddits": ["construction"]
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Fields:**
- `protocol_version` (string, required): A2A protocol version
- `source_agent` (object, required): Information about requesting agent
  - `id` (string): Unique agent identifier
  - `endpoint` (string): Agent's callback endpoint
- `capability` (string, required): Capability being requested
- `payload` (object, required): Request-specific data
- `request_id` (string, required): Unique request identifier (UUID)

### Response Structure

```json
{
  "protocol_version": "1.0",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "validation-agent",
  "capability": "pain_point_validation",
  "status": "success",
  "result": {
    "validation_score": 87,
    "evidence": { /* ... */ }
  }
}
```

**Fields:**
- `protocol_version` (string, required): A2A protocol version
- `request_id` (string, required): Matches request ID
- `agent_id` (string, required): Responding agent's ID
- `capability` (string, required): Capability that was executed
- `status` (string, required): "success" or "error"
- `result` (object, optional): Response data (if success)
- `error` (string, optional): Error message (if error)

## HTTP Headers

All A2A requests must include:

```
Content-Type: application/json
A2A-Protocol-Version: 1.0
A2A-Source-Agent: <agent-id>
```

Optional headers:
```
A2A-Request-Timeout: 30000  (milliseconds)
A2A-Priority: high|normal|low
```

## Endpoints

### Agent Endpoints

Each agent exposes:

- `POST /a2a` - Main A2A endpoint for receiving requests
- `GET /a2a/capabilities` - List supported capabilities
- `GET /a2a/health` - Health check

### Capability Registry

Optional centralized registry:

- `POST /register` - Register agent capabilities
- `GET /discover?capability=X` - Find agents by capability
- `GET /agents` - List all registered agents

## Error Handling

### Error Response Format

```json
{
  "protocol_version": "1.0",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "validation-agent",
  "capability": "pain_point_validation",
  "status": "error",
  "error": "CAPABILITY_NOT_SUPPORTED: pain_point_analysis is not a supported capability"
}
```

### Error Codes

- `INVALID_PROTOCOL_VERSION` - Unsupported protocol version
- `CAPABILITY_NOT_SUPPORTED` - Requested capability not available
- `INVALID_REQUEST` - Malformed request
- `TIMEOUT` - Request exceeded timeout
- `AGENT_UNAVAILABLE` - Target agent not responding
- `INTERNAL_ERROR` - Internal agent error

## Security

### Authentication

Current implementation uses HTTP headers for agent identification. Future versions will support:

1. **API Keys**: Static tokens
2. **JWT Tokens**: Time-limited tokens with claims
3. **mTLS**: Mutual TLS certificate authentication

### Authorization

Agents can implement capability-level authorization:

```json
{
  "capability": "pain_point_validation",
  "allowed_agents": [
    "orchestrator-agent",
    "research-agent"
  ]
}
```

### Request Validation

All requests are validated for:
- Protocol version compatibility
- Request structure
- Payload schema
- Agent identity

## Discovery

### Static Configuration

Agents can be configured with static endpoints:

```bash
export VALIDATION_AGENT_ENDPOINT=https://validation.example.com
export OPPORTUNITY_AGENT_ENDPOINT=https://opportunity.example.com
```

### Dynamic Discovery

Using capability registry:

```python
from shared.a2a_client import A2AClient

client = A2AClient("my-agent", "https://my-agent.com")

# Discover agents with specific capability
agents = client.discover_agents(
    "https://registry.example.com",
    "pain_point_validation"
)

# Use first available agent
result = client.send_request(
    agents[0]["endpoint"],
    "pain_point_validation",
    {"problem": "test"}
)
```

## Timeouts

Default timeouts:
- Request timeout: 60 seconds
- Connection timeout: 10 seconds
- Retry attempts: 3

Configure per-request:
```python
client.send_request(
    target_url,
    capability,
    payload,
    timeout=120  # 2 minutes
)
```

## Examples

### Example 1: Orchestrator → Validation Agent

**Request:**
```http
POST /a2a HTTP/1.1
Host: validation-agent.example.com
Content-Type: application/json
A2A-Protocol-Version: 1.0
A2A-Source-Agent: orchestrator-agent

{
  "protocol_version": "1.0",
  "source_agent": {
    "id": "orchestrator-agent",
    "endpoint": "https://orchestrator.example.com"
  },
  "capability": "pain_point_validation",
  "payload": {
    "problem": "construction equipment tracking",
    "subreddits": ["construction", "contractors"],
    "competitors": ["ToolTracker"],
    "timeframe": "month"
  },
  "request_id": "abc-123-def"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "protocol_version": "1.0",
  "request_id": "abc-123-def",
  "agent_id": "validation-agent",
  "capability": "pain_point_validation",
  "status": "success",
  "result": {
    "validation_score": 87,
    "evidence": { /* ... */ },
    "recommendation": "STRONG VALIDATION"
  }
}
```

### Example 2: Parallel Requests

```python
import asyncio
from orchestrator_agent.tools.agent_router import AgentRouter

router = AgentRouter()

# Analyze multiple opportunities in parallel
results = await router.parallel_analysis([
    {
        "problem": "equipment tracking",
        "market": "construction software",
        "functionality": "tracking with offline"
    },
    {
        "problem": "inventory waste",
        "market": "restaurant software",
        "functionality": "automated inventory"
    }
])
```

## Implementation

### Server Implementation

```python
from shared.a2a_client import A2AServer

# Initialize server
server = A2AServer(
    agent_id="validation-agent",
    capabilities=["pain_point_validation", "competitor_analysis"]
)

# Register handler
def validate_handler(payload):
    # Your validation logic
    return {"validation_score": 87, "evidence": {}}

server.register_handler("pain_point_validation", validate_handler)

# Handle incoming request
@app.post("/a2a")
def handle_a2a(request: dict):
    return server.handle_request(request)
```

### Client Implementation

```python
from shared.a2a_client import A2AClient

# Initialize client
client = A2AClient(
    agent_id="orchestrator-agent",
    agent_endpoint="https://orchestrator.example.com"
)

# Send request
result = client.send_request(
    target_agent_url="https://validation.example.com",
    capability="pain_point_validation",
    payload={
        "problem": "equipment tracking",
        "subreddits": ["construction"]
    }
)
```

## Monitoring

### Metrics

Track these metrics for A2A communication:

- `a2a_requests_total` - Total requests sent/received
- `a2a_request_duration_seconds` - Request latency
- `a2a_errors_total` - Total errors by type
- `a2a_timeouts_total` - Total timeouts

### Logging

Log all A2A interactions:

```json
{
  "timestamp": "2025-01-23T10:30:00Z",
  "event": "a2a_request",
  "source_agent": "orchestrator-agent",
  "target_agent": "validation-agent",
  "capability": "pain_point_validation",
  "request_id": "abc-123",
  "duration_ms": 1234,
  "status": "success"
}
```

## Future Enhancements

Planned for v2.0:
- Bidirectional streaming
- Agent capability negotiation
- Circuit breaker pattern
- Request prioritization
- Result caching
- Webhook notifications

---

## Resources

- [A2A Protocol Official Site](https://a2aprotocol.org)
- [Linux Foundation A2A Spec](https://github.com/a2a-protocol/spec)
- [Google ADK Documentation](https://cloud.google.com/agent-engine/docs)

---

For implementation details, see:
- [API Documentation](API.md)
- [Usage Guide](USAGE.md)
- [Source Code](../shared/a2a_client.py)
