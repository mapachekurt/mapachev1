# Iterable Agent

Expert agent for Iterable operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_590`
Tier: Marketing & Sales
Category: marketing_automation

## Capabilities

- Iterable API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `ITERABLE_API_KEY`: API key for Iterable

### API Configuration

- Base URL: https://api.iterable.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.iterable.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.iterable.agent import iterable_agent

# Execute operations
result = iterable_agent.execute("sync data")

# Get capabilities
capabilities = iterable_agent.get_capabilities()

# Get configuration
config = iterable_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=iterable
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=iterable
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/iterable/tests/
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