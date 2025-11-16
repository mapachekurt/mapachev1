# Nearpod Agent

Expert agent for Nearpod operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1061`
Tier: Specialized Vertical Tools
Category: education

## Capabilities

- Nearpod API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `NEARPOD_API_KEY`: API key for Nearpod

### API Configuration

- Base URL: https://api.nearpod.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.nearpod.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.nearpod.agent import nearpod_agent

# Execute operations
result = nearpod_agent.execute("sync data")

# Get capabilities
capabilities = nearpod_agent.get_capabilities()

# Get configuration
config = nearpod_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=nearpod
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=nearpod
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/nearpod/tests/
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