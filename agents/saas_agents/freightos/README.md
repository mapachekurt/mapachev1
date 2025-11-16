# Freightos Agent

Expert agent for Freightos operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1123`
Tier: Specialized Vertical Tools
Category: logistics

## Capabilities

- Freightos API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `FREIGHTOS_API_KEY`: API key for Freightos

### API Configuration

- Base URL: https://api.freightos.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.freightos.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.freightos.agent import freightos_agent

# Execute operations
result = freightos_agent.execute("sync data")

# Get capabilities
capabilities = freightos_agent.get_capabilities()

# Get configuration
config = freightos_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=freightos
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=freightos
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/freightos/tests/
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