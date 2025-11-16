# Wiki.js Agent

Expert agent for Wiki.js operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_779`
Tier: Productivity & Collaboration
Category: documentation

## Capabilities

- Wiki.js API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `WIKI_JS_API_KEY`: API key for Wiki.js

### API Configuration

- Base URL: https://api.wikijs.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.wikijs.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.wiki_js.agent import wiki_js_agent

# Execute operations
result = wiki_js_agent.execute("sync data")

# Get capabilities
capabilities = wiki_js_agent.get_capabilities()

# Get configuration
config = wiki_js_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=wiki_js
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=wiki_js
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/wiki_js/tests/
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