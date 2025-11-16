# Redash Agent

Expert agent for Redash operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1353`
Tier: Specialized Vertical Tools
Category: bi

## Capabilities

- Redash API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `REDASH_API_KEY`: API key for Redash

### API Configuration

- Base URL: https://api.redash.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.redash.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.redash.agent import redash_agent

# Execute operations
result = redash_agent.execute("sync data")

# Get capabilities
capabilities = redash_agent.get_capabilities()

# Get configuration
config = redash_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=redash
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=redash
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/redash/tests/
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