# Big Cartel Agent

Expert agent for Big Cartel operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_973`
Tier: Specialized Vertical Tools
Category: ecommerce

## Capabilities

- Big Cartel API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `BIG_CARTEL_API_KEY`: API key for Big Cartel

### API Configuration

- Base URL: https://api.bigcartel.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.bigcartel.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.big_cartel.agent import big_cartel_agent

# Execute operations
result = big_cartel_agent.execute("sync data")

# Get capabilities
capabilities = big_cartel_agent.get_capabilities()

# Get configuration
config = big_cartel_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=big_cartel
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=big_cartel
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/big_cartel/tests/
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