# Smallpdf Agent

Expert agent for Smallpdf operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1317`
Tier: Specialized Vertical Tools
Category: utility

## Capabilities

- Smallpdf API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `SMALLPDF_API_KEY`: API key for Smallpdf

### API Configuration

- Base URL: https://api.smallpdf.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.smallpdf.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.smallpdf.agent import smallpdf_agent

# Execute operations
result = smallpdf_agent.execute("sync data")

# Get capabilities
capabilities = smallpdf_agent.get_capabilities()

# Get configuration
config = smallpdf_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=smallpdf
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=smallpdf
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/smallpdf/tests/
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