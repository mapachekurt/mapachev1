# Vendure Agent

Expert agent for Vendure operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_985`
Tier: Specialized Vertical Tools
Category: ecommerce

## Capabilities

- Vendure API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `VENDURE_API_KEY`: API key for Vendure

### API Configuration

- Base URL: https://api.vendure.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.vendure.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.vendure.agent import vendure_agent

# Execute operations
result = vendure_agent.execute("sync data")

# Get capabilities
capabilities = vendure_agent.get_capabilities()

# Get configuration
config = vendure_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=vendure
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=vendure
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/vendure/tests/
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