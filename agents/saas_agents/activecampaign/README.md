# ActiveCampaign Agent

Expert agent for ActiveCampaign operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_535`
Tier: Marketing & Sales
Category: email_marketing

## Capabilities

- ActiveCampaign API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `ACTIVECAMPAIGN_API_KEY`: API key for ActiveCampaign

### API Configuration

- Base URL: https://api.activecampaign.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.activecampaign.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.activecampaign.agent import activecampaign_agent

# Execute operations
result = activecampaign_agent.execute("sync data")

# Get capabilities
capabilities = activecampaign_agent.get_capabilities()

# Get configuration
config = activecampaign_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=activecampaign
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=activecampaign
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/activecampaign/tests/
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