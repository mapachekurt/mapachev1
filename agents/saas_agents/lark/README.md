# Lark (Feishu) Agent

Expert agent for Lark (Feishu) operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1474`
Tier: Specialized Vertical Tools
Category: regional

## Capabilities

- Lark (Feishu) API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `LARK_API_KEY`: API key for Lark (Feishu)

### API Configuration

- Base URL: https://api.lark.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.lark.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.lark.agent import lark_agent

# Execute operations
result = lark_agent.execute("sync data")

# Get capabilities
capabilities = lark_agent.get_capabilities()

# Get configuration
config = lark_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=lark
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=lark
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/lark/tests/
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