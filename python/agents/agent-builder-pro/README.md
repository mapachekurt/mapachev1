# Agent Builder Pro

A RAG-enhanced multi-agent system for building production-ready ADK agents using comprehensive knowledge bases.

## Overview

Agent Builder Pro leverages Gemini File Search RAG with a comprehensive ADK knowledge corpus to guide developers through the complete agent development lifecycle - from requirements gathering to production deployment.

## Architecture

**Type:** Sequential Multi-Agent System with RAG Enhancement

**Root Agent:** Agent Builder Pro Coordinator (gemini-1.5-pro)
**Knowledge Base:** Gemini File Search corpus with ADK documentation, best practices, and code examples

### Sub-Agents

1. **Requirements Gatherer** (gemini-2.0-flash-001)
   - Analyzes user requirements
   - Identifies agent type and architecture needs
   - Extracts constraints and success criteria
   - Outputs structured requirements document

2. **Architecture Designer** (gemini-2.0-flash-001)
   - Designs agent architecture using best practices
   - Selects appropriate agent pattern (Sequential/Parallel/Loop/Custom)
   - Defines sub-agent structure and responsibilities
   - Creates architectural specification

3. **Tool Specification** (gemini-2.0-flash-001)
   - Identifies required tools and integrations
   - Specifies tool interfaces and parameters
   - Validates tool availability and compatibility
   - Generates tool configuration

4. **Code Generator** (gemini-1.5-pro)
   - Generates production-ready agent code
   - Implements best practices and error handling
   - Creates configuration files (config.yaml)
   - Includes comprehensive documentation

5. **Validation & Deployment** (gemini-2.0-flash-001)
   - Validates generated code
   - Creates test files
   - Generates deployment scripts
   - Produces deployment guide

## Features

### RAG Enhancement
- **Knowledge Base:** Comprehensive ADK documentation and best practices
- **File Search:** Gemini File Search integration for accurate retrieval
- **Source Citation:** Agents cite sources from knowledge base
- **Best Practices:** Automated application of ADK patterns and practices

### Agent Development Pipeline
1. Requirements Analysis → 2. Architecture Design → 3. Tool Integration → 4. Code Generation → 5. Validation

### Code Quality
- Production-ready implementations
- Comprehensive error handling
- Type hints and documentation
- Security best practices
- Performance optimization

### Deployment Support
- Vertex AI Agent Engine scripts
- Cloud Run deployment options
- Local testing configurations
- Environment management

## Usage

### Basic Usage

```python
from python.agents.agent_builder_pro import agent_builder_pro_root

# Use the agent
result = agent_builder_pro_root.execute(
    "Build a customer service agent for e-commerce that handles orders, returns, and product questions"
)
```

### With AdkApp

```python
from python.agents.agent_builder_pro import create_agent_builder_pro
from vertexai.agent_engines import AdkApp

# Create agent with RAG
agent = create_agent_builder_pro(
    corpus_resource_name="projects/{project}/locations/{location}/corpora/{corpus_id}"
)

# Create app
app = AdkApp(agent=agent)

# Interactive session
async for event in app.async_stream_query(
    user_id="developer-1",
    message="Create a data analysis agent with visualization capabilities"
):
    print(event)
```

## Configuration

Edit `config.yaml` to customize:
- Model selection
- Knowledge base corpus
- Tool configurations
- Deployment settings

## Knowledge Base

The agent uses a curated knowledge base including:
- **ADK Documentation:** Official guides and references
- **Best Practices:** 8 categories, 30+ patterns
- **Code Examples:** 10+ complete working examples
- **Agent Patterns:** 7 architectural patterns with use cases
- **Deployment Guides:** Vertex AI and Cloud Run deployment

## Output

Agent Builder Pro generates:
1. **Requirements Document:** Structured requirements analysis
2. **Architecture Specification:** Complete architectural design
3. **Tool Configuration:** Tool definitions and integrations
4. **Agent Code:** Production-ready Python implementation
5. **Configuration Files:** config.yaml and related configs
6. **Test Files:** Unit and integration tests
7. **Deployment Scripts:** Scripts for Vertex AI deployment
8. **Documentation:** README and usage guides

## Requirements

```
google-adk>=0.3.0
google-cloud-aiplatform[agent_engines,adk]>=1.112
google-genai>=0.3.0
pydantic>=2.0.0
```

## Environment Variables

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export ADK_CORPUS_RESOURCE_NAME="projects/.../corpora/adk-knowledge-base"
```

## Examples

### Example 1: Simple Customer Service Agent
```
Input: "Create a customer service agent"
Output: Complete agent with greeting, inquiry handling, and escalation logic
```

### Example 2: Complex Data Pipeline Agent
```
Input: "Build a data pipeline agent that extracts, transforms, and analyzes sales data"
Output: Sequential agent with 4 sub-agents for each pipeline stage
```

### Example 3: Multi-Channel Support Agent
```
Input: "Create an agent for handling support across email, chat, and phone"
Output: Parallel agent with channel-specific sub-agents and routing logic
```

## Testing

Run tests:
```bash
python -m pytest python/agents/agent-builder-pro/tests/
```

## Deployment

Deploy to Vertex AI:
```bash
python python/agents/agent-builder-pro/deploy_to_vertex.py
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  Agent Builder Pro Root Agent                    │
│                      (gemini-1.5-pro)                            │
│              [RAG: Gemini File Search Corpus]                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Sequential Pipeline
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼────────┐              ┌──────▼──────┐
│  Requirements   │──────────────▶ Architecture │
│    Gatherer     │              │   Designer   │
└─────────────────┘              └──────┬───────┘
                                        │
                                ┌───────▼────────┐
                                │      Tool      │
                                │ Specification  │
                                └───────┬────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                 ┌───────▼────────┐          ┌────────▼─────────┐
                 │      Code      │──────────▶   Validation &   │
                 │   Generator    │          │    Deployment    │
                 └────────────────┘          └──────────────────┘
```

## Knowledge Base Categories

1. **Agent Architecture** - Patterns and design principles
2. **Tool Integration** - MCP and Python tool patterns
3. **Deployment Strategies** - Vertex AI, Cloud Run, local
4. **Error Handling** - Resilience and recovery patterns
5. **Model Selection** - Flash vs Pro optimization
6. **RAG Integration** - File Search and knowledge bases
7. **Performance** - Optimization techniques
8. **Security** - Best practices and compliance

## Support

For issues or questions:
1. Check the knowledge base documentation
2. Review generated agent examples
3. Consult ADK official documentation
4. Open an issue in the repository

## License

Part of the mapachev1 agent ecosystem.

## Version

1.0.0 - Initial release with RAG enhancement
