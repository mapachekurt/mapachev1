# Zenoti Agent

Expert agent for Zenoti operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1204`
Tier: Specialized Vertical Tools
Category: booking

## Capabilities

- Zenoti API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `ZENOTI_API_KEY`: API key for Zenoti

### API Configuration

- Base URL: https://api.zenoti.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.zenoti.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.zenoti.agent import zenoti_agent

# Execute operations
result = zenoti_agent.execute("sync data")

# Get capabilities
capabilities = zenoti_agent.get_capabilities()

# Get configuration
config = zenoti_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=zenoti
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=zenoti
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/zenoti/tests/
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