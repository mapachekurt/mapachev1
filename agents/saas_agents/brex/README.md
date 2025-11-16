# Brex Agent

Expert agent for Brex operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_914`
Tier: Specialized Vertical Tools
Category: finance

## Capabilities

- Brex API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `BREX_API_KEY`: API key for Brex

### API Configuration

- Base URL: https://api.brex.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.brex.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.brex.agent import brex_agent

# Execute operations
result = brex_agent.execute("sync data")

# Get capabilities
capabilities = brex_agent.get_capabilities()

# Get configuration
config = brex_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=brex
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=brex
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/brex/tests/
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