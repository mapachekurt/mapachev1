# Recruitee Agent

Expert agent for Recruitee operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_943`
Tier: Specialized Vertical Tools
Category: hr

## Capabilities

- Recruitee API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `RECRUITEE_API_KEY`: API key for Recruitee

### API Configuration

- Base URL: https://api.recruitee.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.recruitee.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.recruitee.agent import recruitee_agent

# Execute operations
result = recruitee_agent.execute("sync data")

# Get capabilities
capabilities = recruitee_agent.get_capabilities()

# Get configuration
config = recruitee_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=recruitee
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=recruitee
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/recruitee/tests/
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