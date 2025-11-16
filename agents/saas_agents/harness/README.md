# Harness Agent

Expert agent for Harness operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_633`
Tier: Developer Tools
Category: ci_cd

## Capabilities

- Harness API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `HARNESS_API_KEY`: API key for Harness

### API Configuration

- Base URL: https://api.harness.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.harness.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.harness.agent import harness_agent

# Execute operations
result = harness_agent.execute("sync data")

# Get capabilities
capabilities = harness_agent.get_capabilities()

# Get configuration
config = harness_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=harness
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=harness
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/harness/tests/
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