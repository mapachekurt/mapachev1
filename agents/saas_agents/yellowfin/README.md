# Yellowfin BI Agent

Expert agent for Yellowfin BI operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1367`
Tier: Specialized Vertical Tools
Category: bi

## Capabilities

- Yellowfin BI API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `YELLOWFIN_API_KEY`: API key for Yellowfin BI

### API Configuration

- Base URL: https://api.yellowfin.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.yellowfin.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.yellowfin.agent import yellowfin_agent

# Execute operations
result = yellowfin_agent.execute("sync data")

# Get capabilities
capabilities = yellowfin_agent.get_capabilities()

# Get configuration
config = yellowfin_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=yellowfin
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=yellowfin
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/yellowfin/tests/
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