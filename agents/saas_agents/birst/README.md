# Birst Agent

Expert agent for Birst operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1363`
Tier: Specialized Vertical Tools
Category: bi

## Capabilities

- Birst API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `BIRST_API_KEY`: API key for Birst

### API Configuration

- Base URL: https://api.birst.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.birst.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.birst.agent import birst_agent

# Execute operations
result = birst_agent.execute("sync data")

# Get capabilities
capabilities = birst_agent.get_capabilities()

# Get configuration
config = birst_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=birst
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=birst
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/birst/tests/
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