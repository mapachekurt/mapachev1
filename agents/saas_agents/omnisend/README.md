# Omnisend Agent

Expert agent for Omnisend operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_537`
Tier: Marketing & Sales
Category: email_marketing

## Capabilities

- Omnisend API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `OMNISEND_API_KEY`: API key for Omnisend

### API Configuration

- Base URL: https://api.omnisend.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.omnisend.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.omnisend.agent import omnisend_agent

# Execute operations
result = omnisend_agent.execute("sync data")

# Get capabilities
capabilities = omnisend_agent.get_capabilities()

# Get configuration
config = omnisend_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=omnisend
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=omnisend
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/omnisend/tests/
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