# Linear Agent

Expert agent for Linear operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_525`
Tier: Enterprise Essentials
Category: project_management

## Capabilities

- Linear API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `LINEAR_API_KEY`: API key for Linear

### API Configuration

- Base URL: https://api.linear.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.linear.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.linear.agent import linear_agent

# Execute operations
result = linear_agent.execute("sync data")

# Get capabilities
capabilities = linear_agent.get_capabilities()

# Get configuration
config = linear_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=linear
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=linear
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/linear/tests/
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