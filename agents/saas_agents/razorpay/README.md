# Razorpay Agent

Expert agent for Razorpay operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_927`
Tier: Specialized Vertical Tools
Category: payments

## Capabilities

- Razorpay API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `RAZORPAY_API_KEY`: API key for Razorpay

### API Configuration

- Base URL: https://api.razorpay.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.razorpay.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.razorpay.agent import razorpay_agent

# Execute operations
result = razorpay_agent.execute("sync data")

# Get capabilities
capabilities = razorpay_agent.get_capabilities()

# Get configuration
config = razorpay_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=razorpay
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=razorpay
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/razorpay/tests/
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