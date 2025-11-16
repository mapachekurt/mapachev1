# Census Agent

Expert agent for Census operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1386`
Tier: Specialized Vertical Tools
Category: data

## Capabilities

- Census API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `CENSUS_API_KEY`: API key for Census

### API Configuration

- Base URL: https://api.census.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.census.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.census.agent import census_agent

# Execute operations
result = census_agent.execute("sync data")

# Get capabilities
capabilities = census_agent.get_capabilities()

# Get configuration
config = census_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=census
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=census
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/census/tests/
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