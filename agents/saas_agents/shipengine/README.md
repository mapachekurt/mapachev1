# ShipEngine Agent

Expert agent for ShipEngine operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1115`
Tier: Specialized Vertical Tools
Category: logistics

## Capabilities

- ShipEngine API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SHIPENGINE_API_KEY`: API key for ShipEngine

### API Configuration

- Base URL: https://api.shipengine.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.shipengine.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.shipengine.agent import shipengine_agent

# Execute operations
result = shipengine_agent.execute("sync data")

# Get capabilities
capabilities = shipengine_agent.get_capabilities()

# Get configuration
config = shipengine_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=shipengine
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=shipengine
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/shipengine/tests/
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