# Paylocity Agent

Expert agent for Paylocity operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_955`
Tier: Specialized Vertical Tools
Category: hr

## Capabilities

- Paylocity API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `PAYLOCITY_API_KEY`: API key for Paylocity

### API Configuration

- Base URL: https://api.paylocity.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.paylocity.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.paylocity.agent import paylocity_agent

# Execute operations
result = paylocity_agent.execute("sync data")

# Get capabilities
capabilities = paylocity_agent.get_capabilities()

# Get configuration
config = paylocity_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=paylocity
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=paylocity
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/paylocity/tests/
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