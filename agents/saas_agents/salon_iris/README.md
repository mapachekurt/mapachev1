# Salon Iris Agent

Expert agent for Salon Iris operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1207`
Tier: Specialized Vertical Tools
Category: booking

## Capabilities

- Salon Iris API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SALON_IRIS_API_KEY`: API key for Salon Iris

### API Configuration

- Base URL: https://api.saloniris.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.saloniris.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.salon_iris.agent import salon_iris_agent

# Execute operations
result = salon_iris_agent.execute("sync data")

# Get capabilities
capabilities = salon_iris_agent.get_capabilities()

# Get configuration
config = salon_iris_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=salon_iris
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=salon_iris
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/salon_iris/tests/
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