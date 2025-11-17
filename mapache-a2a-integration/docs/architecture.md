# A2A Protocol Integration - Architecture

## Overview

This document describes the architecture of the A2A Protocol integration for the 511-agent organizational system.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent Registry Service                    │
│  - Agent discovery                                           │
│  - Agent card storage                                        │
│  - Search & filtering                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                        Agent Network                         │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │   CEO    │───▶│   CFO    │───▶│Controller│             │
│  └──────────┘    └──────────┘    └──────────┘             │
│       │               │                                      │
│       ▼               ▼                                      │
│  ┌──────────┐    ┌──────────┐                              │
│  │   CTO    │    │ VP FP&A  │                              │
│  └──────────┘    └──────────┘                              │
│                                                              │
│  ... (378 total agents organized by department)             │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agent Registry Service

**Purpose**: Centralized service for agent discovery and management

**Components**:
- FastAPI web service
- In-memory database (development) / PostgreSQL (production)
- Agent card storage
- Search & filtering engine

**Endpoints**:
- `GET /agents` - List all agents
- `GET /agents/{name}` - Get specific agent
- `POST /agents/search` - Search by skill/department/tag
- `POST /agents/register` - Register new agent
- `GET /health` - Health check

**Storage**:
```python
AGENTS_DB = {
    "ceo": {
        "name": "ceo",
        "description": "...",
        "capabilities": {...},
        "metadata": {...}
    },
    ...
}
```

### 2. BaseA2AAgent

**Purpose**: Foundation class for all agents

**Responsibilities**:
- Initialize ADK agent
- Generate agent card
- Manage hierarchical relationships
- Provide A2A compatibility

**Key Methods**:
- `__init__(config: AgentConfig)` - Initialize agent
- `get_adk_agent()` - Get underlying ADK agent
- `get_agent_card()` - Get agent card
- `save_agent_card()` - Save card to disk
- `add_sub_agent()` - Add managed agent

**Agent Card Structure**:
```json
{
  "name": "agent_name",
  "description": "Agent description",
  "version": "1.0.0",
  "capabilities": {
    "skills": ["skill1", "skill2"],
    "tools": ["tool1", "tool2"],
    "model": "gemini-2.0-flash-exp"
  },
  "metadata": {
    "role": "Role Title",
    "department": "department_name",
    "reports_to": "manager_name",
    "manages": ["report1", "report2"],
    "tags": ["tag1", "tag2"]
  },
  "authentication": {
    "type": "bearer",
    "required": true
  },
  "contact": {
    "email": "agent@mapache.ai"
  }
}
```

### 3. A2AServer

**Purpose**: Expose agents via A2A protocol using FastAPI

**Features**:
- Wraps ADK agent with A2A support using `to_a2a()`
- Adds authentication middleware
- Provides custom endpoints
- Serves agent card at `/.well-known/agent.json`
- CORS configuration

**Server Structure**:
```
FastAPI App
├── Custom Routes
│   ├── GET /                    # Service info
│   ├── GET /health              # Health check
│   ├── GET /.well-known/agent.json  # Agent card
│   └── GET /metrics             # Metrics (authenticated)
└── A2A Routes (from to_a2a())
    ├── POST /message            # Send message to agent
    └── ... (other A2A endpoints)
```

### 4. RemoteAgent

**Purpose**: Client for connecting to remote agents

**Workflow**:
1. Discover agent URL from registry
2. Fetch agent card
3. Establish connection
4. Send messages via A2A protocol

**Features**:
- Automatic discovery
- Retry logic with exponential backoff
- Error handling
- Authentication

## Communication Patterns

### 1. Hierarchical Delegation

**Pattern**: Manager delegates tasks to direct reports

**Example**: CEO → CFO → Controller

```python
# CEO delegates to CFO
ceo_agent = CEOAgent()
ceo_agent.connect_to_leadership_team()
response = ceo_agent.delegate_to_cfo("Review Q4 budget")

# CFO delegates to Controller
cfo_agent = CFOAgent()
cfo_agent.connect_to_finance_team()
response = cfo_agent.delegate_to_controller("Close monthly books")
```

**Benefits**:
- Respects organizational structure
- Clear accountability
- Audit trail

### 2. Peer-to-Peer

**Pattern**: Direct communication between agents at same level

**Example**: Engineering Manager ↔ Product Manager

```python
# PM requests status from EM
pm_agent = RemoteAgent("pm_1_1_1")
response = pm_agent.send_message(
    "What's the status of feature X?",
    context={"feature_id": "FEAT-123"}
)
```

**Benefits**:
- Fast communication
- Collaborative
- Cross-functional

### 3. Coordinator Pattern

**Pattern**: Central coordinator orchestrates multiple agents

**Example**: Product Launch Coordinator

```python
# Product launch coordinator
coordinator = ProductLaunchCoordinator()

# Connect to relevant teams
coordinator.connect_to_team("engineering")
coordinator.connect_to_team("marketing")
coordinator.connect_to_team("sales")

# Orchestrate launch
coordinator.execute_launch_plan()
```

**Benefits**:
- Complex workflows
- Multi-team coordination
- Single point of control

## Agent Discovery Mechanism

### Discovery Flow

```
1. Agent A needs to communicate with Agent B
   │
   ▼
2. Agent A queries Registry for Agent B
   │
   ▼
3. Registry returns Agent B's card (including URL)
   │
   ▼
4. Agent A creates RemoteAgent connection to Agent B
   │
   ▼
5. Agent A sends message to Agent B via A2A protocol
   │
   ▼
6. Agent B processes and responds
```

### Search Capabilities

**By Name**:
```python
agent_card = registry.get_agent("ceo")
```

**By Skill**:
```python
agents = discover_agents_by_skill("financial_planning")
```

**By Department**:
```python
agents = discover_agents_by_department("engineering")
```

**By Tag**:
```python
agents = registry.search(tag="leadership")
```

## Authentication Flow

### Bearer Token Authentication

```
Client
  │
  ├─ Request with Authorization: Bearer <token>
  │
  ▼
Middleware
  │
  ├─ Verify token
  │
  ▼
Agent Endpoint
  │
  └─ Process request
```

### OAuth2 (Future)

For production systems, OAuth2 will provide:
- Token refresh
- Fine-grained permissions
- Audit logging
- Revocation

## MCP + A2A Integration Strategy

### Model Context Protocol (MCP)

Agents can use MCP tools for:
- Database access
- API integrations
- File system operations
- External service calls

### Integration Approach

```python
# Agent with MCP tools
agent = BaseA2AAgent(config)

# MCP tools loaded from config
agent.config.tools = [
    "database_query",
    "api_caller",
    "file_reader"
]

# Tools available via A2A
# Other agents can invoke these tools through this agent
```

### Communication Flow

```
Agent A (needs data)
  │
  ├─ A2A message to Agent B
  │
  ▼
Agent B (has MCP database tool)
  │
  ├─ Uses MCP to query database
  │
  ├─ Formats response
  │
  └─ Returns via A2A to Agent A
```

## Data Flow

### Agent Registration

```
Agent Implementation
  │
  ├─ Define AgentConfig
  │
  ▼
BaseA2AAgent
  │
  ├─ Generate agent card
  │
  ├─ Save to agent_cards/
  │
  ▼
populate_registry.py
  │
  ├─ Read all agent cards
  │
  ├─ POST to registry
  │
  ▼
Registry Service
  │
  └─ Store in AGENTS_DB
```

### Agent Communication

```
Initiating Agent
  │
  ├─ Discover target agent
  │
  ▼
Registry
  │
  ├─ Return agent card with URL
  │
  ▼
RemoteAgent
  │
  ├─ Create connection
  │
  ├─ Send message via A2A
  │
  ▼
Target Agent (A2AServer)
  │
  ├─ Receive message
  │
  ├─ Process with ADK
  │
  ├─ Generate response
  │
  └─ Return via A2A
```

## Scalability Considerations

### Horizontal Scaling

- Each agent deployed independently
- Registry service can be replicated
- Load balancing across agent instances

### Caching

- Agent card caching (reduce registry load)
- Connection pooling
- Response caching for idempotent operations

### Database

- Development: In-memory dictionary
- Production: PostgreSQL with indexes on:
  - Agent name (primary key)
  - Department
  - Skills (GIN index)
  - Tags (GIN index)

## Security Architecture

### Layers of Security

1. **Transport**: HTTPS for all communication
2. **Authentication**: Bearer tokens / OAuth2
3. **Authorization**: Role-based access control
4. **Validation**: Input validation on all endpoints
5. **Rate Limiting**: Prevent abuse
6. **Audit Logging**: Track all agent interactions

### Threat Model

**Threats**:
- Unauthorized agent access
- Message tampering
- Agent impersonation
- Denial of service

**Mitigations**:
- Token-based authentication
- HTTPS encryption
- Agent card signatures (future)
- Rate limiting
- Circuit breakers

## Monitoring & Observability

### Metrics

Each agent exports:
- Request count
- Response latency
- Error rate
- Active connections

### Tracing

OpenTelemetry distributed tracing:
- Trace agent-to-agent calls
- Identify bottlenecks
- Debug issues

### Logging

Structured logging with:
- Request ID
- Agent name
- Timestamp
- Log level
- Message

## Deployment Architecture

### Local Development

```
Developer Machine
├── Registry Service (port 8080)
├── Agent 1 (port 8001)
├── Agent 2 (port 8002)
└── Agent 3 (port 8003)
```

### Production (Google Cloud Run)

```
Cloud Run Services
├── Registry Service (registry.mapache.ai)
├── CEO Agent (ceo.mapache.ai)
├── CFO Agent (cfo.mapache.ai)
└── ... (378 total agent services)

Cloud SQL
└── PostgreSQL (registry database)

Cloud Load Balancing
├── SSL termination
├── DDoS protection
└── Auto-scaling
```

## Future Enhancements

1. **Streaming**: Support streaming responses for long-running tasks
2. **Push Notifications**: Proactive agent notifications
3. **Event Bus**: Publish/subscribe for event-driven workflows
4. **Agent Learning**: Agents learn from interactions
5. **Workflow Engine**: Visual workflow designer
6. **Multi-region**: Deploy agents across regions
7. **Agent Marketplace**: Discover and install community agents
