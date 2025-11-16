# Reddit Ads Agent

Expert agent for Reddit Ads operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_600`
Tier: Marketing & Sales
Category: advertising

## Capabilities

- Reddit Ads API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `REDDIT_ADS_API_KEY`: API key for Reddit Ads

### API Configuration

- Base URL: https://api.redditads.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.redditads.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.reddit_ads.agent import reddit_ads_agent

# Execute operations
result = reddit_ads_agent.execute("sync data")

# Get capabilities
capabilities = reddit_ads_agent.get_capabilities()

# Get configuration
config = reddit_ads_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=reddit_ads
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=reddit_ads
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/reddit_ads/tests/
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