# GnuCash Agent

Expert agent for GnuCash operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_906`
Tier: Specialized Vertical Tools
Category: finance

## Capabilities

- GnuCash API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `GNUCASH_API_KEY`: API key for GnuCash

### API Configuration

- Base URL: https://api.gnucash.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.gnucash.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.gnucash.agent import gnucash_agent

# Execute operations
result = gnucash_agent.execute("sync data")

# Get capabilities
capabilities = gnucash_agent.get_capabilities()

# Get configuration
config = gnucash_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=gnucash
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=gnucash
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/gnucash/tests/
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