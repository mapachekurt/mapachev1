# dbt (Data Build Tool) Agent

Expert agent for dbt (Data Build Tool) operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1384`
Tier: Specialized Vertical Tools
Category: data

## Capabilities

- dbt (Data Build Tool) API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `DBT_API_KEY`: API key for dbt (Data Build Tool)

### API Configuration

- Base URL: https://api.dbt.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.dbt.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.dbt.agent import dbt_agent

# Execute operations
result = dbt_agent.execute("sync data")

# Get capabilities
capabilities = dbt_agent.get_capabilities()

# Get configuration
config = dbt_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=dbt
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=dbt
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/dbt/tests/
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