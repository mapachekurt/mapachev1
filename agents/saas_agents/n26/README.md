# N26 Business Agent

Expert agent for N26 Business operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_937`
Tier: Specialized Vertical Tools
Category: payments

## Capabilities

- N26 Business API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `N26_API_KEY`: API key for N26 Business

### API Configuration

- Base URL: https://api.n26.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.n26.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.n26.agent import n26_agent

# Execute operations
result = n26_agent.execute("sync data")

# Get capabilities
capabilities = n26_agent.get_capabilities()

# Get configuration
config = n26_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=n26
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=n26
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/n26/tests/
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