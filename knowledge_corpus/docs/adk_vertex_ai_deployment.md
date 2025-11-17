# Developing and Deploying ADK Agents to Vertex AI Agent Engine

## Overview

The Agent Development Kit provides a template-based approach to building agents using Google Cloud's Vertex AI Agent Builder. The process centers on the `AdkApp` class from the Vertex AI SDK for Python.

## Core Development Steps

### 1. Model Configuration

Start by specifying your model version:

```python
model = "gemini-2.0-flash"
```

You can optionally configure safety settings and content generation parameters like temperature, max tokens, and top-p values before creating your agent instance.

**Available Models:**
- `gemini-2.0-flash` - Fast, cost-effective for high-volume operations
- `gemini-1.5-flash` - Fast model with good balance
- `gemini-1.5-pro` - Advanced reasoning for complex tasks
- `gemini-1.0-pro` - Stable production model

### 2. Creating an AdkApp Agent

Initialize your agent with required and optional parameters:

```python
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

agent = Agent(
    model=model,
    name='your_agent_name',
    generate_content_config=generate_content_config,  # Optional
)
app = AdkApp(agent=agent)
```

**AdkApp Features:**
- Session management
- Memory management
- Streaming responses
- Integration with Vertex AI services

### 3. Defining and Integrating Tools

Add functions as tools to extend agent capabilities. Tools require clear documentation describing parameters, functionality, and return values.

**Important:** Test tools locally before integration.

```python
def your_function(param: str = "default"):
    """Complete description of function purpose and parameters.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    # Implementation
    return result

agent = Agent(
    model=model,
    name='your_agent_name',
    tools=[your_function],
)
```

**Tool Best Practices:**
- Provide comprehensive docstrings
- Include type hints
- Validate inputs
- Handle errors gracefully
- Return structured data when possible
- Test tools independently

### 4. Testing Locally

Stream queries asynchronously to test agent responses:

```python
async for event in app.async_stream_query(
    user_id="user-123",
    message="Your test query",
):
    print(event)
```

**Testing Best Practices:**
- Test with diverse inputs
- Validate tool calls
- Check error handling
- Monitor latency
- Review response quality

## Advanced Features

### Session Management

Create and manage conversations across sessions:

```python
# Create new session
session = await app.async_create_session(user_id="USER_ID")

# List all sessions for user
sessions = await app.async_list_sessions(user_id="USER_ID")

# Query with session context
async for event in app.async_stream_query(
    user_id="USER_ID",
    session_id=session.id,
    message="Follow-up question",
):
    print(event)
```

**Session Benefits:**
- Maintain conversation context
- Track user interactions
- Enable follow-up questions
- Support multi-turn conversations

### Memory Management

Enable persistent memory with the `PreloadMemoryTool`:

```python
from google import adk

agent = adk.Agent(
    model="gemini-2.0-flash",
    tools=[adk.tools.preload_memory_tool.PreloadMemoryTool()],
)
```

**Memory Operations:**

Generate and search memories from sessions:

```python
# Add session to memory
await app.async_add_session_to_memory(session=session)

# Search memory
response = await app.async_search_memory(
    user_id="USER_ID",
    query="search term"
)
```

**Memory Use Cases:**
- User preferences
- Historical interactions
- Context across sessions
- Personalization
- Learning from past conversations

### Custom Backends

Override default services by implementing `session_service_builder` and `memory_service_builder` functions.

**Note:** Synchronization in distributed deployments requires careful implementation.

```python
def custom_session_service_builder():
    # Your custom session service
    return custom_session_service

def custom_memory_service_builder():
    # Your custom memory service
    return custom_memory_service

app = AdkApp(
    agent=agent,
    session_service_builder=custom_session_service_builder,
    memory_service_builder=custom_memory_service_builder,
)
```

## Deployment to Vertex AI Agent Engine

### Prerequisites

1. **GCP Project Setup:**
   ```bash
   export GOOGLE_CLOUD_PROJECT="your-project-id"
   export GOOGLE_CLOUD_LOCATION="us-central1"
   ```

2. **Enable APIs:**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

3. **Authentication:**
   ```bash
   gcloud auth application-default login
   ```

### Deployment Steps

1. **Package Your Agent:**
   - Ensure all dependencies are in requirements.txt
   - Test locally first
   - Prepare configuration files

2. **Create Deployment:**
   ```python
   from vertexai.agent_engines import deploy_adk_app

   deployment = deploy_adk_app(
       app=app,
       project=PROJECT_ID,
       location=LOCATION,
       staging_bucket=STAGING_BUCKET,
   )
   ```

3. **Configure Endpoints:**
   - Set up authentication
   - Configure rate limiting
   - Enable monitoring

4. **Verify Deployment:**
   - Test deployed agent
   - Monitor logs
   - Validate performance

### Deployment Configuration

**Recommended Configuration:**

```python
deployment_config = {
    "machine_type": "n1-standard-4",
    "min_replica_count": 1,
    "max_replica_count": 10,
    "accelerator_type": None,  # Use TPU/GPU if needed
}
```

## Production Best Practices

### 1. Environment Configuration

Use environment variables for different environments:

```python
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.getenv("ADK_MODEL", "gemini-2.0-flash")
```

### 2. Error Handling

Implement comprehensive error handling:

```python
try:
    async for event in app.async_stream_query(...):
        handle_event(event)
except Exception as e:
    logger.error(f"Query failed: {e}")
    # Implement fallback or retry logic
```

### 3. Monitoring and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log important events
logger.info(f"Agent query: {message}")
logger.info(f"Response generated in {duration}s")
```

### 4. Cost Optimization

- Use Flash models for simple tasks
- Implement caching for frequent queries
- Set appropriate rate limits
- Monitor token usage

### 5. Security

- Use Secret Manager for credentials
- Implement proper IAM roles
- Enable VPC Service Controls
- Audit access logs

## Next Steps After Deployment

1. **Configure Access Controls:**
   - Set up IAM roles
   - Configure authentication
   - Enable audit logging

2. **Implement Tracing and Logging:**
   - Cloud Trace for latency analysis
   - Cloud Logging for debugging
   - Custom metrics for business logic

3. **Evaluate Agent Performance:**
   - Response quality
   - Latency metrics
   - Tool usage patterns
   - Error rates

4. **Continuous Improvement:**
   - Monitor user feedback
   - Iterate on prompts
   - Optimize tool selection
   - Update knowledge bases

## Common Deployment Issues

### Issue: High Latency
**Solution:** Use Flash models, implement caching, optimize prompts

### Issue: High Costs
**Solution:** Right-size model selection, implement rate limiting, use caching

### Issue: Tool Failures
**Solution:** Add retry logic, validate inputs, implement fallbacks

### Issue: Context Issues
**Solution:** Enable session management, use memory tools, optimize prompts

## Resources

- [Vertex AI Agent Engine Documentation](https://cloud.google.com/agent-builder)
- [ADK Python SDK](https://github.com/google/adk-python)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Google Cloud Console](https://console.cloud.google.com/)
