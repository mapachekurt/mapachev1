# ADK Code Examples and Patterns

## Table of Contents
- [Simple LLM Agent](#simple-llm-agent)
- [Sequential Multi-Agent](#sequential-multi-agent)
- [Parallel Multi-Agent](#parallel-multi-agent)
- [Loop Agent](#loop-agent)
- [RAG-Enhanced Agent](#rag-enhanced-agent)
- [Agent with Custom Tools](#agent-with-custom-tools)
- [Complete Application Example](#complete-application-example)

---

## Simple LLM Agent

Basic agent for single-task execution:

```python
from google.adk import Agent

# Create simple agent
agent = Agent(
    name="task_executor",
    instruction="""You are a helpful assistant that analyzes data.
    When given data, provide clear insights and recommendations.""",
    model="gemini-2.0-flash-001"
)

# Use the agent
response = agent.execute("Analyze sales data for Q4 trends")
print(response)
```

---

## Sequential Multi-Agent

Multi-stage pipeline with dependent steps:

```python
from google.adk import Agent, SequentialAgent

# Define sub-agents
requirements_agent = Agent(
    name="requirements_gatherer",
    instruction="""Gather and analyze requirements from user input.
    Extract key features, constraints, and success criteria.
    Output structured requirements.""",
    model="gemini-2.0-flash-001"
)

design_agent = Agent(
    name="architecture_designer",
    instruction="""Design system architecture based on requirements.
    Create component breakdown, data flow, and integration points.
    Output architectural specification.""",
    model="gemini-2.0-flash-001"
)

implementation_agent = Agent(
    name="code_generator",
    instruction="""Generate implementation code based on architecture.
    Follow best practices and include error handling.
    Output production-ready code.""",
    model="gemini-1.5-pro"
)

validation_agent = Agent(
    name="validator",
    instruction="""Validate the implementation.
    Check code quality, test coverage, and compliance.
    Output validation report.""",
    model="gemini-2.0-flash-001"
)

# Create sequential root agent
root_agent = SequentialAgent(
    name="agent_builder",
    instruction="""Build complete agent system from requirements to deployment.
    Coordinate sub-agents to ensure quality output at each stage.""",
    model="gemini-1.5-pro",
    sub_agents=[
        requirements_agent,
        design_agent,
        implementation_agent,
        validation_agent
    ]
)

# Execute pipeline
result = root_agent.execute("Build a customer service agent")
```

---

## Parallel Multi-Agent

Concurrent execution of independent tasks:

```python
from google.adk import Agent, ParallelAgent

# Define parallel sub-agents
technical_analyzer = Agent(
    name="technical_analyzer",
    instruction="Analyze technical feasibility and requirements.",
    model="gemini-2.0-flash-001"
)

business_analyzer = Agent(
    name="business_analyzer",
    instruction="Analyze business value and ROI.",
    model="gemini-2.0-flash-001"
)

risk_analyzer = Agent(
    name="risk_analyzer",
    instruction="Identify and assess risks and mitigation strategies.",
    model="gemini-2.0-flash-001"
)

compliance_analyzer = Agent(
    name="compliance_analyzer",
    instruction="Check regulatory and compliance requirements.",
    model="gemini-2.0-flash-001"
)

# Create parallel root agent
root_agent = ParallelAgent(
    name="comprehensive_analyzer",
    instruction="""Perform comprehensive analysis from multiple perspectives.
    Aggregate insights from all analyses.""",
    model="gemini-1.5-pro",
    sub_agents=[
        technical_analyzer,
        business_analyzer,
        risk_analyzer,
        compliance_analyzer
    ]
)

# Execute parallel analysis
result = root_agent.execute("Analyze new product proposal")
```

---

## Loop Agent

Iterative refinement pattern:

```python
from google.adk import Agent, LoopAgent

# Define generator and reviewer
generator = Agent(
    name="code_generator",
    instruction="""Generate or refine code based on requirements and feedback.
    Improve quality with each iteration.""",
    model="gemini-1.5-pro"
)

reviewer = Agent(
    name="code_reviewer",
    instruction="""Review code for quality, security, and best practices.
    Provide specific feedback for improvement.
    Approve when quality standards are met.""",
    model="gemini-2.0-flash-001"
)

# Create loop agent
root_agent = LoopAgent(
    name="iterative_code_refiner",
    instruction="""Generate and refine code until quality standards are met.
    Continue iterations until approved or max iterations reached.""",
    model="gemini-1.5-pro",
    sub_agents=[generator, reviewer],
    max_iterations=5,
    stop_condition="reviewer approval or quality threshold met"
)

# Execute refinement loop
result = root_agent.execute("Create secure authentication system")
```

---

## RAG-Enhanced Agent

Agent with knowledge base access:

```python
from google.adk import Agent
from google.genai import FileSearchTool

# Configure File Search tool
file_search_tool = FileSearchTool(
    corpus_name="projects/{project}/locations/{location}/corpora/{corpus_id}"
)

# Create RAG-enhanced agent
agent = Agent(
    name="documentation_expert",
    instruction="""You are an expert on Google ADK.
    Answer questions using the knowledge base.
    Always cite sources from the knowledge base.
    Provide code examples when relevant.""",
    model="gemini-1.5-pro",
    tool_config={
        "file_search": {
            "corpus_resource_name": f"projects/{PROJECT_ID}/locations/{LOCATION}/corpora/{CORPUS_ID}"
        }
    }
)

# Use RAG agent
response = agent.execute(
    "How do I create a SequentialAgent with tool integration?"
)
```

---

## Agent with Custom Tools

Integrating Python functions as tools:

```python
from google.adk import Agent, tool
import requests

@tool
def search_documentation(query: str) -> str:
    """Search ADK documentation for relevant information.

    Args:
        query: Search query string

    Returns:
        str: Relevant documentation excerpts
    """
    # Implementation
    results = perform_search(query)
    return format_results(results)

@tool
def create_project_structure(project_name: str, structure_type: str = "agent") -> dict:
    """Create project directory structure.

    Args:
        project_name: Name of the project
        structure_type: Type of structure (agent, saas, fte)

    Returns:
        dict: Created structure information
    """
    # Implementation
    structure = create_directories(project_name, structure_type)
    return {
        "project_name": project_name,
        "structure": structure,
        "status": "created"
    }

@tool
def validate_agent_config(config: dict) -> dict:
    """Validate agent configuration.

    Args:
        config: Agent configuration dictionary

    Returns:
        dict: Validation results with issues and recommendations
    """
    # Implementation
    issues = validate_config(config)
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "recommendations": generate_recommendations(config)
    }

# Create agent with tools
agent = Agent(
    name="agent_development_assistant",
    instruction="""Help developers build ADK agents.
    Use tools to search documentation, create projects, and validate configurations.
    Provide step-by-step guidance with code examples.""",
    model="gemini-1.5-pro",
    tools=[
        search_documentation,
        create_project_structure,
        validate_agent_config
    ]
)

# Use agent with tools
response = agent.execute(
    "Create a new customer service agent project and show me the structure"
)
```

---

## Complete Application Example

End-to-end application with AdkApp:

```python
import os
import asyncio
from google.adk import Agent, SequentialAgent, tool
from vertexai.agent_engines import AdkApp
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

# Environment configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Define custom tools
@tool
def get_user_data(user_id: str) -> dict:
    """Retrieve user data from database."""
    # Implementation
    return {"user_id": user_id, "preferences": {}, "history": []}

@tool
def save_recommendation(user_id: str, recommendation: dict) -> bool:
    """Save recommendation for user."""
    # Implementation
    return True

# Define sub-agents
analyzer = Agent(
    name="user_analyzer",
    instruction="Analyze user data and identify needs.",
    model="gemini-2.0-flash-001",
    tools=[get_user_data]
)

recommender = Agent(
    name="recommendation_engine",
    instruction="Generate personalized recommendations.",
    model="gemini-1.5-pro"
)

executor = Agent(
    name="action_executor",
    instruction="Execute recommended actions.",
    model="gemini-2.0-flash-001",
    tools=[save_recommendation]
)

# Create root agent
root_agent = SequentialAgent(
    name="personalization_agent",
    instruction="""Provide personalized recommendations.
    Analyze user data, generate recommendations, and execute actions.""",
    model="gemini-1.5-pro",
    sub_agents=[analyzer, recommender, executor],
    tools=[PreloadMemoryTool()]
)

# Create application
app = AdkApp(agent=root_agent)

# Async main function
async def main():
    # Create session
    session = await app.async_create_session(user_id="user-123")

    # Interactive loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("Agent: ", end="")
        async for event in app.async_stream_query(
            user_id="user-123",
            session_id=session.id,
            message=user_input,
        ):
            # Handle different event types
            if hasattr(event, "text"):
                print(event.text, end="")
            elif hasattr(event, "tool_call"):
                print(f"\n[Calling tool: {event.tool_call.name}]")

        print("\n")

        # Add to memory periodically
        if should_save_to_memory():
            await app.async_add_session_to_memory(session=session)

# Run application
if __name__ == "__main__":
    asyncio.run(main())
```

---

## Deployment Example

Deploy to Vertex AI Agent Engine:

```python
from vertexai.agent_engines import deploy_adk_app
import os

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"

# Deploy
deployment = deploy_adk_app(
    app=app,
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
    deployment_config={
        "machine_type": "n1-standard-4",
        "min_replica_count": 1,
        "max_replica_count": 10,
    }
)

print(f"Agent deployed: {deployment.resource_name}")
print(f"Endpoint: {deployment.endpoint}")
```

---

## Configuration File Example

config.yaml for agent configuration:

```yaml
agent:
  name: "customer_service_agent"
  model: "gemini-1.5-pro"
  instruction: |
    You are a customer service agent for Acme Corp.
    Help customers with orders, returns, and product questions.
    Always be polite and professional.

sub_agents:
  - name: "order_handler"
    model: "gemini-2.0-flash-001"
    instruction: "Handle order-related inquiries"

  - name: "product_expert"
    model: "gemini-2.0-flash-001"
    instruction: "Answer product questions"

  - name: "returns_processor"
    model: "gemini-2.0-flash-001"
    instruction: "Process returns and refunds"

tools:
  - type: mcp
    server: database
    config:
      connection_string: "${DATABASE_URL}"

  - type: python
    module: "tools.custom_tools"
    functions:
      - search_orders
      - process_refund
      - check_inventory

deployment:
  project: "${GOOGLE_CLOUD_PROJECT}"
  location: "us-central1"
  machine_type: "n1-standard-4"
  min_replicas: 1
  max_replicas: 5
```

---

## Testing Example

Unit tests for agents:

```python
import unittest
from google.adk import Agent

class TestCustomerServiceAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(
            name="test_agent",
            instruction="Test agent for customer service",
            model="gemini-2.0-flash-001"
        )

    def test_order_inquiry(self):
        """Test handling order inquiries."""
        response = self.agent.execute("What's the status of order #12345?")
        self.assertIn("order", response.lower())

    def test_product_question(self):
        """Test answering product questions."""
        response = self.agent.execute("Tell me about Product X")
        self.assertIsNotNone(response)

    def test_error_handling(self):
        """Test error handling."""
        response = self.agent.execute("")
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
```

---

## Best Practices Summary

1. **Agent Design:**
   - Single responsibility per agent
   - Clear, specific instructions
   - Appropriate model selection

2. **Tool Integration:**
   - Comprehensive docstrings
   - Type hints for parameters
   - Error handling and validation

3. **Testing:**
   - Test agents independently
   - Validate tool calls
   - Check error scenarios

4. **Deployment:**
   - Use environment variables
   - Implement proper error handling
   - Monitor and log extensively

5. **Performance:**
   - Use Flash for simple tasks
   - Implement caching
   - Optimize prompts
