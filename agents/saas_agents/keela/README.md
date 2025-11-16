# Keela Agent

Expert agent for Keela operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1264`
Tier: Specialized Vertical Tools
Category: nonprofit

## Capabilities

- Keela API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `KEELA_API_KEY`: API key for Keela

### API Configuration

- Base URL: https://api.keela.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.keela.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.keela.agent import keela_agent

# Execute operations
result = keela_agent.execute("sync data")

# Get capabilities
capabilities = keela_agent.get_capabilities()

# Get configuration
config = keela_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=keela
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=keela
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/keela/tests/
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