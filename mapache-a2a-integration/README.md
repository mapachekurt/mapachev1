# A2A Protocol Integration for 511-Agent Architecture

This project integrates Google's Agent-to-Agent (A2A) Protocol into a comprehensive 511-agent organization, enabling standardized inter-agent communication using Google ADK.

## Overview

The system implements a full organizational hierarchy with 378+ agents across 14 departments, all communicating via the A2A protocol. Each agent can discover, connect to, and collaborate with other agents in the system.

## Project Structure

```
mapache-a2a-integration/
├── agents/                    # Agent implementations
│   ├── core/                 # Core infrastructure (BaseA2AAgent, A2AServer, RemoteAgent)
│   ├── executive/            # Executive agents (CEO, CFO, CTO, etc.)
│   ├── finance/              # Finance department agents
│   ├── sales/                # Sales department agents
│   ├── marketing/            # Marketing department agents
│   ├── engineering/          # Engineering department agents
│   ├── product/              # Product department agents
│   ├── hr/                   # HR department agents
│   ├── operations/           # Operations department agents
│   ├── customer_success/     # Customer success agents
│   ├── data/                 # Data & analytics agents
│   ├── security/             # Security agents
│   ├── it/                   # IT department agents
│   └── facilities/           # Facilities agents
├── infrastructure/
│   ├── registry/             # Agent registry service
│   ├── auth/                 # Authentication
│   └── monitoring/           # Monitoring & observability
├── agent_cards/              # JSON agent cards for all 378 agents
├── scripts/                  # Deployment and utility scripts
├── tests/                    # Test suite
├── docs/                     # Documentation
└── examples/                 # Workflow examples
```

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mapache-a2a-integration
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Generate agent cards (if not already generated):
```bash
python scripts/generate_agent_cards.py
```

### Running Locally

Start the local demo environment:

```bash
./scripts/start_local_demo.sh
```

This will:
- Start the registry service on port 8080
- Populate the registry with all agent cards
- Provide URLs for accessing the services

### Accessing Services

- **Registry**: http://localhost:8080
- **Agent List**: http://localhost:8080/agents (requires Bearer token)
- **Health Check**: http://localhost:8080/health

## Architecture

### Core Components

#### 1. BaseA2AAgent
Foundation class for all agents providing:
- Automatic agent card generation
- ADK integration
- A2A protocol compatibility
- Hierarchical relationships (reports_to, manages)

#### 2. A2AServer
Wraps agents with FastAPI to expose them via A2A:
- Uses ADK's `to_a2a()` for protocol support
- Adds authentication middleware
- Provides health check endpoints
- Serves agent cards at `/.well-known/agent.json`

#### 3. RemoteAgent
Client for connecting to remote agents:
- Discovers agent URLs from registry
- Establishes A2A connections
- Provides message passing capabilities

#### 4. Agent Registry
Centralized service for agent discovery:
- Stores and serves agent cards
- Supports search by skill, department, tags
- Enables dynamic agent discovery

## Agent Organization

The system includes 378 agents organized across 14 departments:

- **Executive** (6 agents): CEO, CFO, CTO, CMO, COO, CHRO
- **Finance** (25 agents): Controllers, FP&A, Treasury, Accountants
- **Sales** (43 agents): Sales Directors, Managers, AEs, SDRs
- **Marketing** (28 agents): Demand Gen, Content, Brand, Creative
- **Engineering** (76 agents): Directors, Managers, Engineers, QA
- **Product** (26 agents): PMs, UX Designers, UI Designers
- **HR** (29 agents): Recruiting, HR Ops, Learning & Development
- **Operations** (27 agents): Operations Managers, Analysts
- **Legal** (9 agents): General Counsel, Attorneys, Paralegals
- **Customer Success** (41 agents): CSMs, Support Agents
- **Data** (26 agents): Data Engineers, Analysts, Scientists
- **Security** (17 agents): Security Engineers, Compliance
- **IT** (15 agents): IT Ops, Infrastructure, Helpdesk
- **Facilities** (10 agents): Office Managers, Coordinators

## Adding a New Agent

### 1. Define Agent Configuration

```python
from agents.core import BaseA2AAgent, AgentConfig

config = AgentConfig(
    name="my_agent",
    description="Description of the agent's role",
    role="Role Title",
    department="department_name",
    skills=["skill1", "skill2", "skill3"],
    tools=["tool1", "tool2"],
    reports_to="manager_agent",
    manages=["report1", "report2"],
    model="gemini-2.0-flash-exp",
)

agent = BaseA2AAgent(config)
```

### 2. Save Agent Card

```python
agent.save_agent_card("agent_cards")
```

### 3. Register with Registry

```bash
python scripts/populate_registry.py
```

## Deployment

### Deploy to Google Cloud Run

Deploy a single agent:

```bash
./scripts/deploy_agent.sh <agent_name>
```

This will:
1. Build a Docker container for the agent
2. Deploy to Google Cloud Run
3. Register the agent with the central registry
4. Configure custom domain

### Environment Variables

Required for production deployment:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
A2A_REGISTRY_URL=https://registry.mapache.ai
BEARER_TOKEN=your-production-token
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run specific test files:

```bash
pytest tests/test_base_agent.py -v
pytest tests/test_registry.py -v
```

## Agent Communication Patterns

### 1. Hierarchical Delegation

CEO delegates to CFO:

```python
from agents.executive.ceo_agent.agent import CEOAgent

ceo = CEOAgent()
ceo.connect_to_leadership_team()
response = ceo.delegate_to_cfo("Review Q4 budget")
```

### 2. Peer-to-Peer Communication

Direct communication between agents:

```python
from agents.core import RemoteAgent

finance_agent = RemoteAgent("cfo")
response = finance_agent.send_message(
    "Need approval for $100k expense",
    context={"department": "engineering", "urgency": "high"}
)
```

### 3. Discovery-Based

Find agents by skill:

```python
from agents.core.remote_agent import discover_agents_by_skill

data_agents = discover_agents_by_skill("data_analysis")
for agent_card in data_agents:
    print(f"Found: {agent_card['name']}")
```

## Authentication

The system uses Bearer token authentication:

1. Set `BEARER_TOKEN` in environment
2. Include in requests: `Authorization: Bearer <token>`
3. All agent endpoints require authentication

## Monitoring & Observability

Each agent exposes:

- **Health endpoint**: `/health`
- **Metrics endpoint**: `/metrics` (authenticated)
- **Agent card**: `/.well-known/agent.json`

## Troubleshooting

### Registry Not Starting

Check logs:
```bash
tail -f logs/registry.log
```

Verify port availability:
```bash
lsof -i :8080
```

### Agent Not Connecting

1. Verify registry is running
2. Check agent card exists in registry
3. Verify authentication token
4. Check network connectivity

### Agent Card Not Found

Regenerate agent cards:
```bash
python scripts/generate_agent_cards.py
python scripts/populate_registry.py
```

## Development

### Running Tests in Development

```bash
# Run with coverage
pytest tests/ --cov=agents --cov=infrastructure --cov-report=html

# Run specific test
pytest tests/test_base_agent.py::test_agent_initialization -v
```

### Adding New Skills

Update `SKILL_DEFINITIONS` in `scripts/generate_agent_cards.py`.

### Modifying Organization Structure

Edit `ORGANIZATIONAL_STRUCTURE` in `scripts/generate_agent_cards.py`, then regenerate cards.

## Production Considerations

1. **Security**:
   - Use strong bearer tokens
   - Enable HTTPS for all endpoints
   - Implement OAuth2 for production

2. **Scalability**:
   - Deploy agents on Cloud Run for auto-scaling
   - Use managed PostgreSQL for registry
   - Implement caching for agent discovery

3. **Reliability**:
   - Add retry logic with exponential backoff
   - Implement circuit breakers
   - Monitor agent health continuously

4. **Observability**:
   - Enable OpenTelemetry tracing
   - Aggregate logs centrally
   - Set up alerting for failures

## Contributing

1. Create feature branch
2. Add tests for new functionality
3. Update documentation
4. Submit pull request

## License

[Your License Here]

## Support

For issues and questions:
- GitHub Issues: [repository]/issues
- Documentation: `docs/`
- Examples: `examples/`
