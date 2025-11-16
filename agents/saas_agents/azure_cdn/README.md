# Azure CDN Agent

Expert agent for Azure CDN operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_657`
Tier: Developer Tools
Category: cloud

## Capabilities

- Azure CDN API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `AZURE_CDN_API_KEY`: API key for Azure CDN

### API Configuration

- Base URL: https://api.azurecdn.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.azurecdn.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.azure_cdn.agent import azure_cdn_agent

# Execute operations
result = azure_cdn_agent.execute("sync data")

# Get capabilities
capabilities = azure_cdn_agent.get_capabilities()

# Get configuration
config = azure_cdn_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=azure_cdn
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=azure_cdn
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/azure_cdn/tests/
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