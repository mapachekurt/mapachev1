# Metabase Agent

Expert agent for Metabase operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1352`
Tier: Specialized Vertical Tools
Category: bi

## Capabilities

- Metabase API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `METABASE_API_KEY`: API key for Metabase

### API Configuration

- Base URL: https://api.metabase.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.metabase.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.metabase.agent import metabase_agent

# Execute operations
result = metabase_agent.execute("sync data")

# Get capabilities
capabilities = metabase_agent.get_capabilities()

# Get configuration
config = metabase_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=metabase
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=metabase
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/metabase/tests/
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