# Expensify Agent

Expert agent for Expensify operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_910`
Tier: Specialized Vertical Tools
Category: finance

## Capabilities

- Expensify API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `EXPENSIFY_API_KEY`: API key for Expensify

### API Configuration

- Base URL: https://api.expensify.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.expensify.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.expensify.agent import expensify_agent

# Execute operations
result = expensify_agent.execute("sync data")

# Get capabilities
capabilities = expensify_agent.get_capabilities()

# Get configuration
config = expensify_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=expensify
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=expensify
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/expensify/tests/
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