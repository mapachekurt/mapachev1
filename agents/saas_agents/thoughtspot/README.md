# ThoughtSpot Agent

Expert agent for ThoughtSpot operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1365`
Tier: Specialized Vertical Tools
Category: bi

## Capabilities

- ThoughtSpot API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `THOUGHTSPOT_API_KEY`: API key for ThoughtSpot

### API Configuration

- Base URL: https://api.thoughtspot.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.thoughtspot.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.thoughtspot.agent import thoughtspot_agent

# Execute operations
result = thoughtspot_agent.execute("sync data")

# Get capabilities
capabilities = thoughtspot_agent.get_capabilities()

# Get configuration
config = thoughtspot_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=thoughtspot
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=thoughtspot
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/thoughtspot/tests/
```

## Integration Status

- [ ] API Integration
- [ ] MCP Server Integration
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Documentation Complete
- [ ] Production Deployment

## Support

For issues or questions, refer to the main [SaaS Agents documentation](../README.md).

## License

Copyright 2025 Mapache - All Rights Reserved