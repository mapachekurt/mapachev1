# Resy Agent

Expert agent for Resy operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1193`
Tier: Specialized Vertical Tools
Category: booking

## Capabilities

- Resy API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `RESY_API_KEY`: API key for Resy

### API Configuration

- Base URL: https://api.resy.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.resy.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.resy.agent import resy_agent

# Execute operations
result = resy_agent.execute("sync data")

# Get capabilities
capabilities = resy_agent.get_capabilities()

# Get configuration
config = resy_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=resy
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=resy
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/resy/tests/
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