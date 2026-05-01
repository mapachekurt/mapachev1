# Scheduled Agent

Expert agent for Scheduled (Fergana-Labs) operations within the Mapache SaaS ecosystem.

## Overview

Agent ID: `agent_1512`
Tier: Productivity & Collaboration
Category: scheduling

Scheduled is an open-source AI scheduling agent that lives in Gmail. When someone emails you to set up a meeting, Scheduled reads the thread, checks your calendar for availability, and drafts a reply with proposed times — all without you lifting a finger.

## Capabilities

- Gmail-based scheduling automation
- Calendar availability checking and draft reply generation
- User scheduling preference learning (bootstrapped from email history)
- Timezone-aware meeting coordination
- Group and 1:1 meeting handling
- Email writing style adaptation
- Follow-up and prioritization handling
- Autopilot mode (auto-send replies)
- Self-hosted deployment on your own infrastructure
- Google OAuth 2.0 authentication

## Configuration

### Environment Variables

- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth client secret
- `ANTHROPIC_API_KEY`: Anthropic Claude API key for AI drafting
- `DATABASE_URL`: Database connection string

### API Configuration

- Source: https://github.com/Fergana-Labs/scheduled
- Documentation: https://github.com/Fergana-Labs/scheduled/blob/main/docs/self-hosting.md

## MCP Server

MCP Server Available: No
Custom integration required

## Usage

```python
from agents.saas_agents.scheduled.agent import scheduled_agent

# Execute operations
result = scheduled_agent.execute("draft scheduling reply")

# Get capabilities
capabilities = scheduled_agent.get_capabilities()

# Get configuration
config = scheduled_agent.get_config()
```

## Deployment

### Development
```bash
# Deploy to dev environment
make deploy-dev AGENT=scheduled
```

### Production
```bash
# Deploy to production
make deploy-prod AGENT=scheduled
```

## Testing

```bash
# Run tests
pytest agents/saas_agents/scheduled/tests/
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
