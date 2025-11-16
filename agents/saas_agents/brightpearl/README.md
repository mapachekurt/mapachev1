# Brightpearl Agent

Expert agent for Brightpearl operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1147`
Tier: Specialized Vertical Tools
Category: inventory

## Capabilities

- Brightpearl API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `BRIGHTPEARL_API_KEY`: API key for Brightpearl

### API Configuration

- Base URL: https://api.brightpearl.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.brightpearl.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.brightpearl.agent import brightpearl_agent

# Execute operations
result = brightpearl_agent.execute("sync data")

# Get capabilities
capabilities = brightpearl_agent.get_capabilities()

# Get configuration
config = brightpearl_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=brightpearl
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=brightpearl
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/brightpearl/tests/
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