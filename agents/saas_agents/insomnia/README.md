# Insomnia Agent

Expert agent for Insomnia operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_711`
Tier: Developer Tools
Category: api

## Capabilities

- Insomnia API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `INSOMNIA_API_KEY`: API key for Insomnia

### API Configuration

- Base URL: https://api.insomnia.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.insomnia.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.insomnia.agent import insomnia_agent

# Execute operations
result = insomnia_agent.execute("sync data")

# Get capabilities
capabilities = insomnia_agent.get_capabilities()

# Get configuration
config = insomnia_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=insomnia
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=insomnia
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/insomnia/tests/
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