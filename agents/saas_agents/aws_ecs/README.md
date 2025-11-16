# AWS ECS Agent

Expert agent for AWS ECS operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_646`
Tier: Developer Tools
Category: cloud

## Capabilities

- AWS ECS API integration
- Real-time data synchronization
- Workflow automation
- OAuth authentication (planned)
- Error handling and recovery
- Rate limiting management

## Configuration

### Environment Variables

- `AWS_ECS_API_KEY`: API key for AWS ECS

### API Configuration

- Base URL: https://api.awsecs.com
- Rate Limit: 1000 requests/hour
- Documentation: https://docs.awsecs.com

## MCP Server


MCP Server Available: No
Custom integration required


## Usage

```python
from agents.saas_agents.aws_ecs.agent import aws_ecs_agent

# Execute operations
result = aws_ecs_agent.execute("sync data")

# Get capabilities
capabilities = aws_ecs_agent.get_capabilities()

# Get configuration
config = aws_ecs_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=aws_ecs
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=aws_ecs
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/aws_ecs/tests/
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