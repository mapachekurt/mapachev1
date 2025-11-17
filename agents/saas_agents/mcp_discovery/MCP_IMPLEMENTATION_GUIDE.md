# MCP Implementation Guide
## Phase 2: Model Context Protocol Integration

**Document Version**: 1.0
**Last Updated**: 2025-11-17
**Status**: Phase 2 - MCP Discovery Complete, Integration In Progress

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [MCP Discovery Results](#mcp-discovery-results)
3. [Integration Strategy](#integration-strategy)
4. [Implementation Phases](#implementation-phases)
5. [Technical Architecture](#technical-architecture)
6. [Integration Patterns](#integration-patterns)
7. [Priority Matrix](#priority-matrix)
8. [Next Steps](#next-steps)

---

## Executive Summary

### What We've Accomplished

Phase 2 MCP Discovery has successfully cataloged **32 of 1000 agents** (3.2%) with comprehensive API and MCP server availability research:

- **15 MCP servers found** (1.5% of agents have existing MCP servers)
- **32 APIs documented** (all researched agents have public APIs)
- **17/20 Tier 1 agents researched** (85% complete)
- **Critical AI platforms researched** (OpenAI, Anthropic, Hugging Face, Cohere, Replicate)

### Key Findings

1. **Official MCP Ecosystem is Growing**:
   - `modelcontextprotocol/servers` repository has 15+ official servers
   - Major partners (Zapier, Figma, Auth0) have MCP servers
   - Community momentum is strong

2. **High-Priority Gaps Identified**:
   - Gmail, Google Calendar, Google Sheets need custom MCP servers
   - Microsoft Teams, Outlook need custom MCP servers
   - Linear needs custom GraphQL MCP server
   - Most Tier 2-5 agents need custom servers

3. **Three Integration Paths**:
   - **Path A**: Direct MCP integration (15 agents ready)
   - **Path B**: Build custom MCP servers (17+ high-priority agents)
   - **Path C**: Direct API integration (968 remaining agents)

---

## MCP Discovery Results

### Agents with Existing MCP Servers (15)

| Priority | Agent ID | Name | MCP Server | Status |
|----------|----------|------|------------|--------|
| ⭐⭐⭐ Critical | 526 | GitHub | `modelcontextprotocol/servers/github` | ✅ Ready |
| ⭐⭐⭐ Critical | 527 | GitLab | `modelcontextprotocol/servers/gitlab` | ✅ Ready |
| ⭐⭐⭐ Critical | 1452 | OpenAI | `mzxrai/mcp-openai` | ✅ Ready |
| ⭐⭐⭐ Critical | 1453 | Anthropic | `anthropic/mcp-anthropic` | ✅ Ready |
| ⭐⭐ High | 518 | Google Drive | `modelcontextprotocol/servers/google-drive` | ✅ Ready |
| ⭐⭐ High | 638 | AWS S3 | `modelcontextprotocol/servers/aws-s3` | ✅ Ready |
| ⭐⭐ High | 639 | AWS Lambda | `modelcontextprotocol/servers/aws-lambda` | ✅ Ready |
| ⭐⭐ High | 733 | PostgreSQL | `modelcontextprotocol/servers/postgres` | ✅ Ready |
| ⭐⭐ High | 757 | Figma | `figma/mcp-server` | ✅ Ready |
| ⭐⭐ High | 1328 | Zapier | `zapier/mcp-server` | ✅ Ready |
| ⭐⭐ High | 1432 | Auth0 | `modelcontextprotocol/servers/auth0` | ✅ Ready |
| ⭐ Medium | 653 | Azure Storage | `modelcontextprotocol/servers/azure-storage` | ✅ Ready |
| ⭐ Medium | 732 | MongoDB | `community/mcp-mongodb` | ✅ Ready |
| ⭐ Medium | 734 | MySQL | `community/mcp-mysql` | ✅ Ready |
| ⭐ Medium | 735 | Redis | `modelcontextprotocol/servers/redis` | ✅ Ready |

### High-Priority Agents Needing Custom MCP Servers (17)

| Priority | Agent ID | Name | API Type | Auth | Complexity |
|----------|----------|------|----------|------|------------|
| ⭐⭐⭐ | 516 | Gmail | Gmail API | OAuth | Medium |
| ⭐⭐⭐ | 517 | Google Calendar | Calendar API | OAuth | Medium |
| ⭐⭐⭐ | 519 | Google Sheets | Sheets API | OAuth | Medium |
| ⭐⭐⭐ | 521 | Outlook | Graph API | OAuth | Medium |
| ⭐⭐⭐ | 525 | Linear | GraphQL | API Key | Low |
| ⭐⭐⭐ | 1454 | Hugging Face | REST API | API Key | Low |
| ⭐⭐ | 512 | Microsoft Teams | Graph API | OAuth | High |
| ⭐⭐ | 513 | Discord | Discord API | OAuth/Bot | Medium |
| ⭐⭐ | 520 | Google Docs | Docs API | OAuth | Medium |
| ⭐⭐ | 522 | OneDrive | Graph API | OAuth | Medium |
| ⭐⭐ | 523 | SharePoint | Graph/REST API | OAuth | High |
| ⭐⭐ | 1455 | Cohere | REST API | API Key | Low |
| ⭐⭐ | 1456 | Replicate | REST API | API Key | Low |
| ⭐ | 514 | Webex | REST API | OAuth | Medium |
| ⭐ | 515 | Google Meet | Workspace APIs | OAuth | Medium |
| ⭐ | 529 | Teams Admin | Graph API | OAuth | High |
| ⭐ | 530 | Workspace Admin | Admin SDK | OAuth | High |

---

## Integration Strategy

### Three-Phased Approach

#### Phase 2A: Quick Wins (Week 1-2)
**Goal**: Integrate agents with existing MCP servers

- **Agents**: 15 with existing MCP servers
- **Effort**: Low (client integration only)
- **Impact**: High (immediate value, proven integrations)
- **Dependencies**: Node.js, npx, authentication tokens

**Deliverables**:
- ✅ MCP client integration template
- Agent implementations using MCP clients
- Integration tests
- Documentation

#### Phase 2B: Custom MCP Servers (Week 3-6)
**Goal**: Build custom MCP servers for high-priority APIs

- **Agents**: 17 critical/high priority agents
- **Effort**: Medium-High (server development)
- **Impact**: Critical (Gmail, Linear, Microsoft Teams, etc.)
- **Dependencies**: API credentials, OAuth setup

**Deliverables**:
- ✅ Custom MCP server template
- Server implementations for top 10 agents
- Testing framework
- Deployment configurations

#### Phase 2C: Direct API Integration (Week 7+)
**Goal**: Integrate remaining agents via direct API calls

- **Agents**: 968 remaining agents
- **Effort**: Low-Medium per agent (template-based)
- **Impact**: Complete coverage
- **Dependencies**: API keys, OAuth framework

**Deliverables**:
- Direct API integration templates
- Bulk generation scripts
- Testing automation
- Documentation

---

## Technical Architecture

### MCP Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mapache Agent Ecosystem                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Agent 526  │    │  Agent 516  │    │  Agent XYZ  │     │
│  │   GitHub    │    │    Gmail    │    │   Other     │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                   │                   │             │
│         │                   │                   │             │
│  ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐     │
│  │ MCP Client  │    │ MCP Client  │    │   Direct    │     │
│  │ Integration │    │ Integration │    │ API Call    │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                   │                   │             │
├─────────┼───────────────────┼───────────────────┼───────────┤
│         │                   │                   │             │
│  ┌──────▼──────┐    ┌──────▼──────┐            │             │
│  │   Existing  │    │   Custom    │            │             │
│  │ MCP Server  │    │ MCP Server  │            │             │
│  │  (GitHub)   │    │  (Gmail)    │            │             │
│  └──────┬──────┘    └──────┬──────┘            │             │
│         │                   │                   │             │
├─────────┼───────────────────┼───────────────────┼───────────┤
│         │                   │                   │             │
│  ┌──────▼──────────────────▼───────────────────▼──────┐     │
│  │              External SaaS APIs                     │     │
│  │  (GitHub API, Gmail API, Linear API, etc.)         │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

1. **Agent Layer** (`agent.py`)
   - Business logic
   - Task orchestration
   - Response formatting

2. **MCP Client Integration**
   - Connect to MCP servers
   - Discover capabilities
   - Execute tool calls

3. **MCP Server Layer** (when custom)
   - Tool definitions
   - Resource definitions
   - Prompt templates
   - API abstraction

4. **SaaS API Layer**
   - HTTP/GraphQL clients
   - Authentication
   - Rate limiting
   - Error handling

---

## Integration Patterns

### Pattern 1: Existing MCP Server Integration

**Use when**: MCP server already exists (15 agents)

**Example**: GitHub Agent

```python
from mcp_client_integration import MCPIntegratedAgent

async def github_agent():
    agent = MCPIntegratedAgent(
        agent_id="agent_526",
        agent_name="github",
        mcp_server_command="npx",
        mcp_server_args=["-y", "@modelcontextprotocol/server-github"]
    )

    async with agent:
        # List repositories
        repos = await agent.call_tool("list_repositories",
                                      {"username": "mapachekurt"})

        # Create issue
        issue = await agent.call_tool("create_issue", {
            "owner": "mapachekurt",
            "repo": "mapachev1",
            "title": "Feature request",
            "body": "Description"
        })
```

**Pros**:
- ✅ Production-ready servers
- ✅ Maintained by MCP community
- ✅ Low implementation effort
- ✅ Standardized interface

**Cons**:
- ❌ Requires Node.js runtime
- ❌ Limited customization
- ❌ Dependency on external packages

### Pattern 2: Custom MCP Server

**Use when**: API exists but no MCP server (17+ high-priority agents)

**Example**: Gmail Server

```python
from custom_mcp_server_template import CustomMCPServer

class GmailMCPServer(CustomMCPServer):
    def __init__(self, oauth_token):
        super().__init__(
            name="gmail-server",
            version="1.0.0",
            api_base_url="https://gmail.googleapis.com/gmail/v1",
            oauth_token=oauth_token
        )

    def _register_tools(self):
        # Define Gmail-specific tools
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(name="send_email", ...),
                Tool(name="list_messages", ...),
                Tool(name="read_message", ...),
            ]
```

**Pros**:
- ✅ Full control over implementation
- ✅ Custom optimizations
- ✅ Tailored to specific use cases
- ✅ Python-native (no Node.js)

**Cons**:
- ❌ Higher development effort
- ❌ Maintenance burden
- ❌ Testing overhead

### Pattern 3: Direct API Integration

**Use when**: Simple APIs, low priority, or specialized use cases

**Example**: Simple REST API

```python
class DirectAPIAgent:
    def __init__(self, api_key):
        self.client = httpx.AsyncClient(
            base_url="https://api.example.com",
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def execute_operation(self, operation, params):
        response = await self.client.post(f"/{operation}", json=params)
        return response.json()
```

**Pros**:
- ✅ Simple implementation
- ✅ No MCP overhead
- ✅ Direct control
- ✅ Lightweight

**Cons**:
- ❌ No standardization
- ❌ No MCP benefits (prompts, resources)
- ❌ Less discoverable

---

## Priority Matrix

### Immediate (Week 1-2) - Path A

| Agent ID | Name | Action | Complexity | Impact |
|----------|------|--------|------------|--------|
| 526 | GitHub | Integrate existing MCP | Low | Critical |
| 527 | GitLab | Integrate existing MCP | Low | Critical |
| 1452 | OpenAI | Integrate existing MCP | Low | Critical |
| 1453 | Anthropic | Integrate existing MCP | Low | Critical |
| 518 | Google Drive | Integrate existing MCP | Low | High |
| 757 | Figma | Integrate existing MCP | Low | High |
| 1328 | Zapier | Integrate existing MCP | Low | High |

### Short-term (Week 3-6) - Path B

| Agent ID | Name | Action | Complexity | Impact |
|----------|------|--------|------------|--------|
| 516 | Gmail | Build custom MCP | Medium | Critical |
| 517 | Calendar | Build custom MCP | Medium | Critical |
| 525 | Linear | Build custom MCP | Low | Critical |
| 519 | Sheets | Build custom MCP | Medium | High |
| 521 | Outlook | Build custom MCP | Medium | High |
| 512 | Teams | Build custom MCP | High | High |

### Medium-term (Week 7+) - Path C

| Tier | Agents | Action | Complexity | Priority |
|------|--------|--------|------------|----------|
| Tier 2 | 90 | Direct API + templates | Medium | High |
| Tier 3 | 113 | Direct API + templates | Medium | Medium |
| Tier 4 | 149 | Direct API + templates | Low | Medium |
| Tier 5 | 613 | Direct API + templates | Low | Low |

---

## OAuth Integration

### OAuth Flow Implementation

Many high-priority agents require OAuth 2.0:

**Google Services** (Gmail, Calendar, Sheets, Docs, Drive):
- Provider: Google OAuth 2.0
- Scopes: Service-specific
- SDK: `google-auth`, `google-auth-oauthlib`

**Microsoft Services** (Teams, Outlook, OneDrive, SharePoint):
- Provider: Microsoft Identity Platform
- Scopes: Graph API permissions
- SDK: `msal` (Microsoft Authentication Library)

**Implementation Template**:

```python
from google_auth_oauthlib.flow import Flow

class OAuthManager:
    def __init__(self, client_id, client_secret, scopes):
        self.flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=scopes
        )

    def get_authorization_url(self):
        auth_url, _ = self.flow.authorization_url(prompt='consent')
        return auth_url

    def exchange_code_for_token(self, code):
        self.flow.fetch_token(code=code)
        return self.flow.credentials
```

---

## Next Steps

### Immediate Actions (This Week)

1. **✅ Complete Phase 2 Discovery**
   - [x] Research Tier 1 agents
   - [x] Research AI platforms
   - [x] Catalog MCP servers
   - [x] Create integration templates

2. **⏳ Begin Path A Implementation**
   - [ ] Set up MCP client infrastructure
   - [ ] Integrate GitHub agent (Agent 526)
   - [ ] Integrate GitLab agent (Agent 527)
   - [ ] Write integration tests
   - [ ] Document deployment process

3. **⏳ Prepare Path B Foundation**
   - [ ] Set up OAuth infrastructure (Google, Microsoft)
   - [ ] Create Gmail MCP server prototype
   - [ ] Create Linear MCP server prototype
   - [ ] Establish testing framework

### Week 2-3 Goals

4. **Path A Completion**
   - [ ] Integrate all 15 agents with existing MCP servers
   - [ ] Complete integration testing
   - [ ] Deploy to dev environment
   - [ ] Performance benchmarking

5. **Path B Prototypes**
   - [ ] Complete Gmail MCP server
   - [ ] Complete Linear MCP server
   - [ ] Complete Google Calendar MCP server
   - [ ] Integration testing

### Month 2 Goals

6. **Path B Scale-Up**
   - [ ] Complete all 17 custom MCP servers
   - [ ] OAuth implementation for Google Workspace
   - [ ] OAuth implementation for Microsoft 365
   - [ ] Production deployment (top 10 agents)

7. **Path C Preparation**
   - [ ] Direct API integration templates
   - [ ] Bulk generation automation
   - [ ] Begin Tier 2 implementation

---

## Resources

### Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)

### Templates
- `/mcp_discovery/templates/mcp_client_integration.py` - MCP client template
- `/mcp_discovery/templates/custom_mcp_server_template.py` - Custom server template

### Discovery Artifacts
- `/mcp_discovery/mcp_availability_tracker.yaml` - Full tracking data
- `/mcp_discovery/discovery_report.md` - Discovery findings
- `/mcp_discovery/discoveries.json` - Machine-readable discoveries

---

## Success Metrics

### Phase 2A (MCP Integration)
- [ ] 15 agents integrated with existing MCP servers
- [ ] 100% test coverage for integrated agents
- [ ] < 2s average response time
- [ ] Deployed to dev environment

### Phase 2B (Custom Servers)
- [ ] 10 custom MCP servers built
- [ ] OAuth working for Google + Microsoft
- [ ] Documentation complete
- [ ] Deployed to staging environment

### Phase 2C (API Integration)
- [ ] 100 Tier 2 agents integrated
- [ ] Templates validated across diverse APIs
- [ ] Automation pipeline working
- [ ] Path to 1000 agent completion clear

---

**Document Maintained By**: Mapache Development Team
**Last Review**: 2025-11-17
**Next Review**: 2025-11-24
