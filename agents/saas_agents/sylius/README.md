# Sylius Agent

Expert agent for Sylius operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_983`
Tier: Specialized Vertical Tools
Category: ecommerce

## Capabilities

- Sylius API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SYLIUS_API_KEY`: API key for Sylius

### API Configuration

- Base URL: https://api.sylius.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.sylius.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.sylius.agent import sylius_agent

# Execute operations
result = sylius_agent.execute("sync data")

# Get capabilities
capabilities = sylius_agent.get_capabilities()

# Get configuration
config = sylius_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=sylius
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=sylius
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/sylius/tests/
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