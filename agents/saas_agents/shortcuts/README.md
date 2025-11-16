# Shortcuts Software Agent

Expert agent for Shortcuts Software operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1206`
Tier: Specialized Vertical Tools
Category: booking

## Capabilities

- Shortcuts Software API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SHORTCUTS_API_KEY`: API key for Shortcuts Software

### API Configuration

- Base URL: https://api.shortcuts.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.shortcuts.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.shortcuts.agent import shortcuts_agent

# Execute operations
result = shortcuts_agent.execute("sync data")

# Get capabilities
capabilities = shortcuts_agent.get_capabilities()

# Get configuration
config = shortcuts_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=shortcuts
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=shortcuts
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/shortcuts/tests/
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