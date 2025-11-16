# ShippingEasy Agent

Expert agent for ShippingEasy operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1120`
Tier: Specialized Vertical Tools
Category: logistics

## Capabilities

- ShippingEasy API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SHIPPINGEASY_API_KEY`: API key for ShippingEasy

### API Configuration

- Base URL: https://api.shippingeasy.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.shippingeasy.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.shippingeasy.agent import shippingeasy_agent

# Execute operations
result = shippingeasy_agent.execute("sync data")

# Get capabilities
capabilities = shippingeasy_agent.get_capabilities()

# Get configuration
config = shippingeasy_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=shippingeasy
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=shippingeasy
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/shippingeasy/tests/
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