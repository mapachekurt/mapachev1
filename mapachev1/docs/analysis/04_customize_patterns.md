# Agent Starter Pack: Comprehensive Customization Patterns Guide

## Table of Contents
1. [Overview](#overview)
2. [Template Extension Mechanisms](#template-extension-mechanisms)
3. [Custom Tool Integration Patterns](#custom-tool-integration-patterns)
4. [Multi-Agent Orchestration Approaches](#multi-agent-orchestration-approaches)
5. [Agent Hierarchy and Design Patterns](#agent-hierarchy-and-design-patterns)
6. [Session and State Management](#session-and-state-management)
7. [Tool Development Guidelines](#tool-development-guidelines)
8. [Best Practices for Extending Templates](#best-practices-for-extending-templates)

---

## Overview

The Agent Starter Pack follows a "Bring Your Own Agent" philosophy, providing production-ready infrastructure while allowing complete customization of agent logic. It supports multiple frameworks:

- **Google ADK (Agent Development Kit)**: Official Google framework for building agents
- **LangGraph**: Graph-based agent orchestration
- **CrewAI**: Multi-agent collaboration framework
- **Custom Implementations**: Full flexibility for custom approaches

### Available Agent Templates

| Template | Framework | Use Case | Key Features |
|----------|-----------|----------|--------------|
| `adk_base` | Google ADK | General-purpose conversational agents | ReAct pattern, tool integration, simple setup |
| `adk_a2a_base` | Google ADK + A2A Protocol | Distributed agent communication | Agent interoperability, microservices architecture |
| `agentic_rag` | Google ADK + LangChain | Document retrieval and Q&A | RAG pipeline, Vertex AI Search/Vector Search integration |
| `langgraph_base_react` | LangGraph | Graph-based reasoning | State management, streaming, control flow |
| `crewai_coding_crew` | CrewAI + LangGraph | Multi-agent collaboration | Agent delegation, sequential task processing |
| `adk_live` | Google ADK | Real-time multimodal interaction | Audio/video/text processing, WebSocket support |

---

## Template Extension Mechanisms

### 1. Creating Remote Templates

Remote templates allow you to package custom agent logic into reusable, shareable Git repositories.

#### Repository Structure

```
my-awesome-template/
├── pyproject.toml                 # Dependencies and configuration
├── uv.lock                        # Locked dependencies (recommended)
├── app/
│   ├── __init__.py
│   └── agent.py                   # Your custom agent logic
├── tests/
│   ├── unit/
│   │   └── test_agent.py
│   └── integration/
│       └── test_agent.py
├── deployment/
│   └── terraform/
│       ├── custom.tf              # Custom infrastructure
│       └── dev/
│           └── custom.tf          # Dev-specific overrides
├── notebooks/
│   └── agent_exploration.ipynb
├── README.md                      # Usage and setup instructions
└── Makefile                       # Custom build targets (optional)
```

#### Configuration File: `pyproject.toml`

```toml
[project]
name = "my-awesome-template"
version = "0.1.0"
description = "A custom agent template for specific use cases"
authors = [{name = "Your Name", email = "your@email.com"}]
dependencies = [
    "google-adk>=1.15.0,<2.0.0",
    "your-custom-package>=1.0.0",
]
requires-python = ">=3.10,<3.13"

[tool.agent-starter-pack]
# Base template to inherit from (users can override with --base-template)
base_template = "adk_base"

# Template metadata (falls back to [project] section if omitted)
name = "My Awesome Template"
description = "An awesome AI agent template with custom features"

# Example question shown to users
example_question = "What does your agent do?"

# Configuration settings
[tool.agent-starter-pack.settings]
# Deployment targets this template supports
deployment_targets = ["agent_engine", "cloud_run"]

# Customize the directory name for agent files (default: "app")
agent_directory = "app"

# Whether to include data ingestion pipeline
requires_data_ingestion = false

# Whether to require session storage selection
requires_session = true

# Frontend type to include
frontend_type = "None"  # or "streamlit", "adk_live_react", etc.

# Interactive command to run after creation
interactive_command = "make playground"

# Custom tags for categorization
tags = ["adk", "custom"]

# Custom dependencies (only for built-in templates)
# For remote templates, use [project].dependencies instead
extra_dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.3.4,<9.0.0",
    "pytest-asyncio>=0.23.8,<1.0.0",
]

[project.optional-dependencies]
streamlit = ["streamlit>=1.42.0,<2.0.0"]
jupyter = ["jupyter>=1.0.0,<2.0.0"]

[tool.pytest.ini_options]
pythonpath = "."
asyncio_default_fixture_loop_scope = "function"
```

#### Version Locking for Compatibility

Lock your template to a specific Agent Starter Pack version to ensure compatibility:

```toml
[dependency-groups]
dev = [
    "agent-starter-pack==0.14.1",  # Lock to specific version
    "pytest>=8.3.4",
]
```

Users will then get guaranteed compatibility:
```bash
uvx agent-starter-pack==0.14.1 create my-project -a your-template-repo
```

#### Creating and Publishing Remote Templates

1. **Create the template structure** with your custom agent logic
2. **Add pyproject.toml** with dependencies and configuration
3. **Test locally**:
   ```bash
   uvx agent-starter-pack create test-project -a local@./your-template
   ```
4. **Publish to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial remote template"
   git remote add origin https://github.com/your-username/my-awesome-template
   git push -u origin main
   ```
5. **Users can now use it**:
   ```bash
   uvx agent-starter-pack create my-project -a https://github.com/your-username/my-awesome-template
   ```

#### File Merging Order

When using a remote template, files are merged in this order (later overwrites earlier):

1. **Base Template Files** - Foundational files from the starter pack
2. **Deployment Target Files** - Target-specific files (cloud_run, agent_engine)
3. **Frontend Files** - Optional UI components
4. **Base Agent Files** - Application logic from the base template
5. **Remote Template Files** (Highest Priority) - Your repository's files override everything

This means your custom `app/agent.py` will replace the base template's version.

#### Makefile Customization in Remote Templates

If your template includes a `Makefile`, it will be intelligently merged:
- Your commands take precedence
- New unique commands are added
- Base commands are preserved

Example custom Makefile:
```makefile
# Custom deployment target
deploy-custom:
	@echo "Deploying with custom configuration"
	gcloud run deploy my-agent --region us-central1

# Override the playground command
playground:
	@echo "Starting custom playground"
	uv run streamlit run custom_app.py
```

### 2. Customizing Infrastructure with Terraform

Add custom infrastructure without replacing base files:

```
deployment/terraform/
├── custom_services.tf           # New services (merged)
├── providers.tf                 # Overrides base providers.tf
└── dev/
    └── custom_dev_setup.tf      # Dev-specific additions
```

Example custom Terraform:
```hcl
# deployment/terraform/custom_services.tf
resource "google_storage_bucket" "custom_bucket" {
  name          = "${var.project_id}-custom-data"
  location      = "US"
  
  uniform_bucket_level_access = true
}

resource "google_pubsub_topic" "agent_events" {
  name = "${var.project_id}-agent-events"
}
```

---

## Custom Tool Integration Patterns

### 1. Basic Tool Definition (ADK Pattern)

Tools are Python functions with type annotations and docstrings:

```python
# app/agent.py
from google.adk.agents import Agent
from google.adk.apps.app import App

def get_weather(location: str) -> str:
    """Get current weather for a location.
    
    Args:
        location: The city or region name
        
    Returns:
        Weather information as a string
    """
    # Your implementation here
    if "san francisco" in location.lower():
        return "It's 60 degrees and foggy"
    return "It's 70 degrees and sunny"


def search_documents(query: str, max_results: int = 5) -> str:
    """Search through a knowledge base.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        Formatted search results as a string
    """
    # Implementation
    return f"Found {max_results} documents for '{query}'"


# Create agent with tools
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Use your tools to answer questions.",
    tools=[get_weather, search_documents],  # Pass functions directly
)

app = App(root_agent=root_agent, name="app")
```

### 2. Advanced Tool Patterns with Context

#### Tool with External Service Integration

```python
import os
from typing import Optional
from google.cloud import aiplatform
from google.adk.agents import Agent
from google.adk.apps.app import App

# Initialize services at module level
vertexai_project = os.environ.get("GOOGLE_CLOUD_PROJECT")
vertexai_region = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

class DocumentRetriever:
    """Manages document retrieval from Vertex AI Search."""
    
    def __init__(self, datastore_id: str, project_id: str, region: str):
        self.datastore_id = datastore_id
        self.project_id = project_id
        self.region = region
        self._client = None
    
    def retrieve(self, query: str, max_results: int = 5) -> str:
        """Retrieve relevant documents."""
        try:
            # Implementation here
            return f"Retrieved {max_results} documents for: {query}"
        except Exception as e:
            return f"Error retrieving documents: {str(e)}"


retriever = DocumentRetriever(
    datastore_id=os.environ.get("DATA_STORE_ID", "default"),
    project_id=vertexai_project,
    region=vertexai_region
)


def retrieve_docs(query: str) -> str:
    """Retrieve relevant documents based on a query.
    
    Use this when you need additional information to answer a question.
    
    Args:
        query: The user's question or search query
        
    Returns:
        Formatted string containing relevant document content
    """
    return retriever.retrieve(query, max_results=5)


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant for question-answering tasks.",
    tools=[retrieve_docs],
)

app = App(root_agent=root_agent, name="app")
```

#### Tool with LangChain Components (RAG Pattern)

```python
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
from langchain_google_community import VertexAISearchRetriever
from langchain_google_community.vertex_rank import VertexAIRank
from langchain_core.prompts import PromptTemplate
from google.adk.agents import Agent
from google.adk.apps.app import App
import os

# Initialize LangChain components
embedding = VertexAIEmbeddings(
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location="us-central1",
    model_name="text-embedding-005"
)

retriever = VertexAISearchRetriever(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    data_store_id=os.environ.get("DATA_STORE_ID"),
    location_id="us",
    engine_data_type=1,
    max_documents=10,
)

compressor = VertexAIRank(
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location_id="global",
    ranking_config="default_ranking_config",
    top_n=5,
)

# Template for formatting documents
format_docs = PromptTemplate.from_template(
    """## Context provided:
{% for doc in docs%}
<Document {{ loop.index0 }}>
{{ doc.page_content | safe }}
</Document {{ loop.index0 }}>
{% endfor %}
""",
    template_format="jinja2",
)


def retrieve_and_rank_docs(query: str) -> str:
    """Retrieve and rank relevant documents.
    
    Args:
        query: The search query
        
    Returns:
        Formatted documents with highest relevance scores first
    """
    try:
        # Retrieve documents
        retrieved_docs = retriever.invoke(query)
        
        # Re-rank with Vertex AI Rank
        ranked_docs = compressor.compress_documents(
            documents=retrieved_docs,
            query=query
        )
        
        # Format for LLM consumption
        formatted = format_docs.format(docs=ranked_docs)
        return formatted
    except Exception as e:
        return f"Error retrieving documents: {str(e)}"


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a QA assistant. Use provided context to answer questions.",
    tools=[retrieve_and_rank_docs],
)

app = App(root_agent=root_agent, name="app")
```

### 3. Tool Definition Pattern for LangGraph Agents

```python
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

LLM = "gemini-2.5-flash"
llm = ChatVertexAI(model=LLM, location="global", temperature=0)


@tool
def fetch_news(topic: str) -> str:
    """Fetch latest news on a topic.
    
    Args:
        topic: The topic to search for
        
    Returns:
        News articles as formatted text
    """
    # Implementation
    return f"News about {topic}"


@tool
def translate_text(text: str, target_language: str) -> str:
    """Translate text to target language.
    
    Args:
        text: The text to translate
        target_language: The target language code (e.g., 'es', 'fr')
        
    Returns:
        Translated text
    """
    # Implementation
    return f"Translated: {text}"


# Create ReAct agent with LangGraph
agent = create_react_agent(
    model=llm,
    tools=[fetch_news, translate_text],
    prompt="You are a helpful assistant with access to news and translation tools."
)
```

### 4. Tool Definition Pattern for CrewAI

```python
from crewai import Agent, Task, Crew, Process
from langchain_google_vertexai import ChatVertexAI

# Define tools for the crew
def code_generator(requirements: str) -> str:
    """Generate Python code based on requirements."""
    # Implementation
    return f"Generated code for: {requirements}"


def test_generator(code: str) -> str:
    """Generate unit tests for given code."""
    # Implementation
    return f"Generated tests for the provided code"


# Create specialized agents
senior_engineer = Agent(
    role="Senior Software Engineer",
    goal="Write clean, efficient Python code",
    backstory="Expert Python developer with 10+ years experience",
    tools=[code_generator],
    allow_delegation=False,
    verbose=True,
    llm="vertex_ai/gemini-2.5-flash"
)

qa_engineer = Agent(
    role="QA Engineer",
    goal="Ensure code quality and test coverage",
    backstory="Thorough QA engineer focused on testing",
    tools=[test_generator],
    allow_delegation=True,
    verbose=True,
    llm="vertex_ai/gemini-2.5-flash"
)

# Define tasks
code_task = Task(
    description="Write Python code for user requirements",
    agent=senior_engineer,
    expected_output="Clean, well-documented Python code"
)

test_task = Task(
    description="Write comprehensive unit tests",
    agent=qa_engineer,
    expected_output="Complete test suite with good coverage"
)

# Create crew
dev_crew = Crew(
    agents=[senior_engineer, qa_engineer],
    tasks=[code_task, test_task],
    process=Process.sequential,
    verbose=True
)
```

### 5. Tool Definition for ADK Live (Multimodal Tools)

```python
import os
from google.adk.agents import Agent
from google.adk.apps.app import App

def process_audio_query(audio_data: str) -> str:
    """Process audio input and return transcription.
    
    Args:
        audio_data: Base64-encoded audio data
        
    Returns:
        Transcribed text from audio
    """
    # Vertex AI Speech-to-Text integration
    return "Transcribed audio content"


def generate_response(text: str) -> str:
    """Generate a response to user input.
    
    Args:
        text: The user's text input
        
    Returns:
        Generated response
    """
    return f"Response to: {text}"


root_agent = Agent(
    name="root_agent",
    model="gemini-live-2.5-flash-preview-native-audio-09-2025",
    instruction="You are a helpful multimodal assistant.",
    tools=[process_audio_query, generate_response],
)

app = App(root_agent=root_agent, name="app")
```

---

## Multi-Agent Orchestration Approaches

### 1. CrewAI Multi-Agent Pattern

CrewAI enables specialized agents to collaborate on complex tasks through delegation and sequential/hierarchical processing.

#### Basic Multi-Agent Crew Setup

```python
# app/crew/crew.py
from typing import Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class DevCrew:
    """Developer crew for collaborative coding."""

    # Load configuration from YAML files
    agents_config: dict[str, Any]
    tasks_config: dict[str, Any]

    # Model configuration
    llm = "vertex_ai/gemini-2.5-flash"

    @agent
    def senior_engineer(self) -> Agent:
        """Senior engineer responsible for implementation."""
        return Agent(
            config=self.agents_config.get("senior_engineer"),
            allow_delegation=False,  # Won't delegate tasks
            verbose=True,
            llm=self.llm,
        )

    @agent
    def qa_engineer(self) -> Agent:
        """QA engineer responsible for testing."""
        return Agent(
            config=self.agents_config.get("qa_engineer"),
            allow_delegation=True,   # Can delegate to senior engineer
            verbose=True,
            llm=self.llm,
        )

    @task
    def code_task(self) -> Task:
        """Task for code generation."""
        return Task(
            config=self.tasks_config.get("code_task"),
            agent=self.senior_engineer(),
        )

    @task
    def test_task(self) -> Task:
        """Task for test generation."""
        return Task(
            config=self.tasks_config.get("test_task"),
            agent=self.qa_engineer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates and returns the crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # Execute tasks one by one
            verbose=True,
        )


# app/agent.py - Integrate crew into main agent
from langgraph.prebuilt import create_react_agent
from langchain_google_vertexai import ChatVertexAI
from .crew.crew import DevCrew

llm = ChatVertexAI(model="gemini-2.5-flash", location="global", temperature=0)


def execute_coding_task(requirements: str) -> str:
    """Use the crew to handle coding tasks.
    
    Args:
        requirements: User's coding requirements
        
    Returns:
        Generated code with tests
    """
    crew = DevCrew()
    inputs = {"requirements": requirements}
    result = crew.crew().kickoff(inputs=inputs)
    return result


# Main agent uses the crew as a tool
agent = create_react_agent(
    model=llm,
    tools=[execute_coding_task],
    prompt="You are a lead engineer manager. Use your team to solve coding problems."
)
```

#### YAML Configuration for Crew (Optional)

```yaml
# app/crew/config/agents.yaml
senior_engineer:
  role: Senior Software Engineer
  goal: Write production-ready Python code
  backstory: |
    You are an expert Python engineer with 15+ years of experience.
    You write clean, efficient, well-documented code.

qa_engineer:
  role: QA Engineer
  goal: Ensure high-quality, well-tested code
  backstory: |
    You are a meticulous QA engineer focused on code quality.
    You write comprehensive tests with excellent coverage.

# app/crew/config/tasks.yaml
code_task:
  description: |
    Write Python code to implement the user's requirements.
    Think about edge cases and error handling.
  expected_output: Clean, production-ready Python code with docstrings

test_task:
  description: |
    Write comprehensive unit tests for the provided code.
    Aim for >80% code coverage.
  expected_output: Complete test file with pytest assertions
```

### 2. LangGraph Multi-Agent Pattern

LangGraph provides fine-grained control over multi-agent orchestration through explicit state management and graph definitions.

```python
# app/agent.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool

llm = ChatVertexAI(model="gemini-2.5-flash", location="global")


# Define shared state
class AgentState(TypedDict):
    user_input: str
    research_findings: str
    analysis: str
    final_response: str


# Define specialized agents
@tool
def research_tool(query: str) -> str:
    """Research a topic and return findings."""
    return f"Research findings for: {query}"


@tool
def analysis_tool(data: str) -> str:
    """Analyze data and return insights."""
    return f"Analysis of: {data}"


def research_node(state: AgentState) -> AgentState:
    """Research node - gathers initial information."""
    from langgraph.prebuilt import create_react_agent
    
    agent = create_react_agent(llm, tools=[research_tool])
    result = agent.invoke({"messages": [("user", state["user_input"])]})
    
    state["research_findings"] = result
    return state


def analysis_node(state: AgentState) -> AgentState:
    """Analysis node - analyzes research findings."""
    from langgraph.prebuilt import create_react_agent
    
    agent = create_react_agent(llm, tools=[analysis_tool])
    result = agent.invoke(
        {"messages": [("user", f"Analyze: {state['research_findings']}")]}
    )
    
    state["analysis"] = result
    return state


def synthesis_node(state: AgentState) -> AgentState:
    """Synthesis node - creates final response."""
    final_prompt = f"""
    Based on:
    - Research: {state['research_findings']}
    - Analysis: {state['analysis']}
    
    Provide a comprehensive final response.
    """
    
    result = llm.invoke(final_prompt)
    state["final_response"] = str(result.content)
    return state


# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("analysis", analysis_node)
workflow.add_node("synthesis", synthesis_node)

# Define edges
workflow.add_edge(START, "research")
workflow.add_edge("research", "analysis")
workflow.add_edge("analysis", "synthesis")
workflow.add_edge("synthesis", END)

# Compile the graph
agent = workflow.compile()
```

### 3. ADK Agent-to-Agent Communication (A2A Protocol)

The A2A protocol enables distributed agent communication and interoperability.

```python
# app/agent.py
import os
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor

# Define your agent with description for interoperability
root_agent = Agent(
    name="data_processor",
    model="gemini-2.5-flash",
    description="An agent that can process and analyze data from other agents",
    instruction="""You are a data processing agent. You receive queries from other agents
    and provide processed results. Always return structured responses.""",
    tools=[],  # Can have tools, but also accepts input from other agents
)

app = App(root_agent=root_agent, name="app")


# The FastAPI integration handles A2A communication automatically
# See fast_api_app.py for A2A endpoint setup
```

#### A2A Protocol Integration in FastAPI

The A2A protocol is automatically integrated in `fast_api_app.py` when `is_adk_a2a` is true:

```python
# This is handled automatically in the generated fast_api_app.py
from a2a.server.apps import A2AFastAPIApplication
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from google.adk.a2a.utils.agent_card_builder import AgentCardBuilder

# The agent card is built dynamically from root_agent
agent_card = await AgentCardBuilder(
    agent=adk_app.root_agent,
    capabilities=AgentCapabilities(streaming=True),
    rpc_url=f"{APP_URL}/a2a/app",
).build()

# A2A endpoints are automatically registered
a2a_app = A2AFastAPIApplication(agent_card=agent_card, http_handler=request_handler)
```

---

## Agent Hierarchy and Design Patterns

### 1. Single Agent with Tool-Based Hierarchy

```python
# app/agent.py
from google.adk.agents import Agent
from google.adk.apps.app import App

class CompanyDataService:
    """Service for accessing company data."""
    
    def get_employees(self, department: str) -> str:
        return f"Employees in {department}"
    
    def get_finances(self) -> str:
        return "Financial summary"


data_service = CompanyDataService()


def query_employees(department: str) -> str:
    """Query employees by department."""
    return data_service.get_employees(department)


def get_financials() -> str:
    """Get financial information."""
    return data_service.get_financials()


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""You are a company assistant with access to employee and financial data.
    Use your tools to answer questions about the organization.""",
    tools=[query_employees, get_financials],
)

app = App(root_agent=root_agent, name="app")
```

### 2. Hierarchical Multi-Agent Pattern with CrewAI

```python
# app/crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Any


@CrewBase
class ResearchCrew:
    """Multi-level research crew with hierarchy."""
    
    agents_config: dict[str, Any]
    tasks_config: dict[str, Any]
    llm = "vertex_ai/gemini-2.5-flash"
    
    # Level 1: Research Team
    @agent
    def researcher_one(self) -> Agent:
        return Agent(
            config=self.agents_config.get("researcher_one"),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    @agent
    def researcher_two(self) -> Agent:
        return Agent(
            config=self.agents_config.get("researcher_two"),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
    
    # Level 2: Lead Researcher (can delegate to researchers)
    @agent
    def lead_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config.get("lead_researcher"),
            allow_delegation=True,  # Can delegate to researchers
            verbose=True,
            llm=self.llm,
        )
    
    # Level 3: Report Writer (uses lead researcher's findings)
    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config.get("report_writer"),
            allow_delegation=True,  # Can delegate to lead researcher
            verbose=True,
            llm=self.llm,
        )
    
    # Define tasks in hierarchical order
    @task
    def research_task_1(self) -> Task:
        return Task(
            config=self.tasks_config.get("research_1"),
            agent=self.researcher_one(),
        )
    
    @task
    def research_task_2(self) -> Task:
        return Task(
            config=self.tasks_config.get("research_2"),
            agent=self.researcher_two(),
        )
    
    @task
    def coordinate_research(self) -> Task:
        return Task(
            config=self.tasks_config.get("coordinate"),
            agent=self.lead_researcher(),
        )
    
    @task
    def write_report(self) -> Task:
        return Task(
            config=self.tasks_config.get("write_report"),
            agent=self.report_writer(),
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # Execute in order
            verbose=True,
        )
```

### 3. Conditional Routing with LangGraph

Route requests to different agents based on content:

```python
# app/agent.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END, router
from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(model="gemini-2.5-flash", location="global")


class RequestState(TypedDict):
    user_input: str
    request_type: str  # "technical", "business", "general"
    response: str


def classify_request(state: RequestState) -> RequestState:
    """Classify the type of request."""
    classification_prompt = f"""
    Classify this request as one of: technical, business, general
    Request: {state['user_input']}
    
    Respond with ONLY the category (one word).
    """
    result = llm.invoke(classification_prompt)
    state["request_type"] = str(result.content).strip().lower()
    return state


def technical_agent_node(state: RequestState) -> RequestState:
    """Handle technical requests."""
    prompt = f"Technical question: {state['user_input']}\nProvide technical details."
    result = llm.invoke(prompt)
    state["response"] = str(result.content)
    return state


def business_agent_node(state: RequestState) -> RequestState:
    """Handle business requests."""
    prompt = f"Business question: {state['user_input']}\nProvide business insights."
    result = llm.invoke(prompt)
    state["response"] = str(result.content)
    return state


def general_agent_node(state: RequestState) -> RequestState:
    """Handle general requests."""
    prompt = f"General question: {state['user_input']}\nProvide a helpful response."
    result = llm.invoke(prompt)
    state["response"] = str(result.content)
    return state


def route_request(state: RequestState) -> str:
    """Route to the appropriate agent."""
    request_type = state.get("request_type", "general")
    if request_type == "technical":
        return "technical_agent"
    elif request_type == "business":
        return "business_agent"
    else:
        return "general_agent"


# Build workflow
workflow = StateGraph(RequestState)
workflow.add_node("classify", classify_request)
workflow.add_node("technical_agent", technical_agent_node)
workflow.add_node("business_agent", business_agent_node)
workflow.add_node("general_agent", general_agent_node)

workflow.add_edge(START, "classify")
workflow.add_conditional_edges(
    "classify",
    route_request,
    {
        "technical_agent": "technical_agent",
        "business_agent": "business_agent",
        "general_agent": "general_agent",
    },
)
workflow.add_edge("technical_agent", END)
workflow.add_edge("business_agent", END)
workflow.add_edge("general_agent", END)

agent = workflow.compile()
```

---

## Session and State Management

### 1. Session Management in ADK Agents

The ADK provides multiple session storage options.

#### In-Memory Sessions (Development)

```python
# app/agent.py - Default for local development
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name="my-app"
)
```

#### AlloyDB Sessions (Cloud SQL)

Configured in `fast_api_app.py` when deployment target is `cloud_run`:

```python
# deployment/terraform/terraform.tfvars or environment
db_user = "postgres"
db_name = "agent_sessions"
db_pass = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")

# Connection string
session_service_uri = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

# Used in FastAPI app
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=session_service_uri,
)
```

#### Agent Engine Sessions

For `agent_engine` deployment target:

```python
import os
from vertexai import agent_engines

# Get or create agent in Agent Engine
agent_name = os.environ.get("AGENT_ENGINE_SESSION_NAME", "my-agent")
existing = list(agent_engines.list(filter=f"display_name={agent_name}"))

if existing:
    agent_engine = existing[0]
else:
    agent_engine = agent_engines.create(display_name=agent_name)

session_service_uri = f"agentengine://{agent_engine.resource_name}"

app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=session_service_uri,
)
```

### 2. Session Lifecycle Management

```python
# Testing with sessions
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


def test_with_session():
    """Example of session lifecycle management."""
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a new session
    session = session_service.create_session_sync(
        user_id="test_user",
        app_name="my-app"
    )
    
    # Create runner
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="my-app"
    )
    
    # Run agent with streaming
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Hello, how are you?")]
    )
    
    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        )
    )
    
    # Process events
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Response: {part.text}")
    
    return session
```

### 3. State Management in LangGraph Agents

```python
# app/agent.py
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage


class AgentState(TypedDict):
    """Complete state for the agent execution."""
    messages: list[BaseMessage]
    user_id: str
    session_id: str
    context: dict  # Custom context
    step_count: int


def process_input(state: AgentState) -> AgentState:
    """Process user input and update state."""
    state["step_count"] += 1
    
    # Add context to state
    state["context"]["last_step"] = "process_input"
    state["context"]["timestamp"] = datetime.now().isoformat()
    
    return state


def run_agent(state: AgentState) -> AgentState:
    """Run the main agent logic."""
    response = agent.invoke({
        "messages": state["messages"],
        "user_id": state["user_id"],
    })
    
    state["messages"].append(response)
    return state


def persist_session(state: AgentState) -> AgentState:
    """Persist session state to storage."""
    # Store in database or session service
    session_data = {
        "user_id": state["user_id"],
        "session_id": state["session_id"],
        "messages": [msg.dict() for msg in state["messages"]],
        "context": state["context"],
        "step_count": state["step_count"],
    }
    
    # Save to storage
    # db.save_session(session_data)
    
    return state


workflow = StateGraph(AgentState)
workflow.add_node("process", process_input)
workflow.add_node("run_agent", run_agent)
workflow.add_node("persist", persist_session)

workflow.add_edge(START, "process")
workflow.add_edge("process", "run_agent")
workflow.add_edge("run_agent", "persist")
workflow.add_edge("persist", END)

agent = workflow.compile()
```

---

## Tool Development Guidelines

### 1. Tool Best Practices

```python
# Good: Clear, well-documented tools with proper types
from typing import Optional
from google.adk.agents import Agent

def search_documents(
    query: str,
    filter_category: Optional[str] = None,
    max_results: int = 10,
) -> str:
    """Search through documents with optional filtering.
    
    This tool is used when you need to find specific documents
    or information that isn't in your immediate knowledge.
    
    Args:
        query: The search query string (required)
        filter_category: Optional category to filter results by
        max_results: Maximum number of results to return (default: 10)
        
    Returns:
        A formatted string containing the search results, with each
        result on a new line showing title, relevance score, and summary
        
    Raises:
        ValueError: If query is empty or max_results is negative
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if max_results < 0:
        raise ValueError("max_results must be non-negative")
    
    # Implementation
    results = []
    try:
        # Search logic here
        pass
    except Exception as e:
        return f"Error during search: {str(e)}"
    
    return "\n".join(results)


root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="Use your tools to search for information.",
    tools=[search_documents],
)
```

### 2. Error Handling in Tools

```python
import logging
from typing import Union

logger = logging.getLogger(__name__)


def fetch_external_data(source_id: str) -> Union[str, dict]:
    """Fetch data from external source with proper error handling.
    
    Args:
        source_id: The ID of the data source
        
    Returns:
        Formatted data as string or error message
    """
    try:
        # Validate input
        if not source_id:
            return "Error: source_id is required"
        
        # Attempt to fetch data
        # result = external_api.fetch(source_id)
        
        # Validate result
        if not result:
            logger.warning(f"No data found for source: {source_id}")
            return f"No data available for source: {source_id}"
        
        # Log successful operation
        logger.info(f"Successfully fetched data for source: {source_id}")
        
        return str(result)
        
    except TimeoutError:
        logger.error(f"Timeout fetching source {source_id}")
        return "Error: Request timed out. Please try again."
    
    except PermissionError:
        logger.error(f"Permission denied accessing source {source_id}")
        return "Error: You don't have permission to access this source."
    
    except Exception as e:
        logger.exception(f"Unexpected error fetching source {source_id}")
        return f"Error: {type(e).__name__}: {str(e)}"
```

### 3. Tool with Caching

```python
from functools import lru_cache
import hashlib
from datetime import datetime, timedelta

class CachedToolService:
    """Tool service with caching for expensive operations."""
    
    def __init__(self, cache_ttl_seconds: int = 3600):
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self.cache = {}
    
    def _cache_key(self, **kwargs) -> str:
        """Generate cache key from parameters."""
        key_str = "|".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cached value is still valid."""
        return datetime.now() - timestamp < self.cache_ttl
    
    def get_data(self, query: str, **kwargs) -> str:
        """Get data with caching.
        
        Args:
            query: The search query
            **kwargs: Additional filter parameters
            
        Returns:
            Cached or freshly fetched data
        """
        cache_key = self._cache_key(query=query, **kwargs)
        
        # Check cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return f"(cached) {data}"
        
        # Fetch fresh data
        data = self._fetch_data(query, **kwargs)
        
        # Store in cache
        self.cache[cache_key] = (data, datetime.now())
        
        return data
    
    def _fetch_data(self, query: str, **kwargs) -> str:
        """Actual data fetching logic."""
        # Implementation
        return f"Data for: {query}"


# Usage in agent
service = CachedToolService(cache_ttl_seconds=1800)  # 30 minutes


def get_data_cached(query: str, category: str = "all") -> str:
    """Get cached data.
    
    Args:
        query: Search query
        category: Data category (default: all)
        
    Returns:
        Formatted data (may be cached)
    """
    return service.get_data(query=query, category=category)
```

### 4. Async Tool Support (for high-performance scenarios)

```python
import asyncio
from typing import Coroutine


async def async_compute_intensive_task(data: str) -> str:
    """Perform async computation without blocking.
    
    Args:
        data: Input data to process
        
    Returns:
        Processed result
    """
    # Simulate async work
    await asyncio.sleep(2)
    return f"Processed: {data}"


# Note: Most agent frameworks handle async automatically
# when tools are defined as async functions
def compute_wrapper(data: str) -> str:
    """Wrapper for async tool in sync context."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_compute_intensive_task(data))
```

### 5. Tool Unit Testing

```python
import pytest
from google.adk.agents.run_config import RunConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService


def test_tool_with_valid_input():
    """Test tool with valid input."""
    result = search_documents("test query", max_results=5)
    assert isinstance(result, str)
    assert len(result) > 0


def test_tool_with_invalid_input():
    """Test tool with invalid input."""
    result = search_documents("", max_results=5)
    assert "Error" in result or result == ""


def test_agent_integration():
    """Test tool integration with agent."""
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(
        user_id="test_user",
        app_name="test"
    )
    
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="test"
    )
    
    # Test agent interaction
    from google.genai import types
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Search for python tips")]
    )
    
    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=session.id,
            run_config=RunConfig(),
        )
    )
    
    assert len(events) > 0
```

---

## Best Practices for Extending Templates

### 1. Project Structure Best Practices

```
my-custom-agent/
├── .gitignore
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── pyproject.toml
├── uv.lock
├── app/
│   ├── __init__.py
│   ├── agent.py                    # Main agent definition
│   ├── tools.py                    # Tool definitions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── retriever.py            # RAG/retrieval logic
│   │   ├── processor.py            # Data processing
│   │   └── external_api.py         # External integrations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py              # Pydantic models
│   │   └── types.py                # Custom types
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Configuration
│   ├── app_utils/
│   │   ├── __init__.py
│   │   ├── tracing.py              # Already provided
│   │   ├── gcs.py                  # Already provided
│   │   └── custom_utils.py         # Your utilities
│   └── prompts/
│       ├── __init__.py
│       ├── system_prompts.py       # System prompt templates
│       └── few_shot.py             # Few-shot examples
├── tests/
│   ├── unit/
│   │   ├── test_tools.py
│   │   └── test_services.py
│   └── integration/
│       ├── test_agent.py           # Already provided
│       └── test_integration.py
├── notebooks/
│   ├── exploration.ipynb
│   └── evaluation.ipynb
├── deployment/
│   ├── terraform/
│   │   ├── variables.tf            # Already provided
│   │   └── custom.tf               # Your infrastructure
│   └── README.md
├── docs/
│   ├── SETUP.md
│   ├── USAGE.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── Makefile                        # Already provided - customize
├── README.md
└── GEMINI.md                       # Use with Gemini CLI
```

### 2. Configuration Management Pattern

```python
# app/config/settings.py
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class RAGSettings:
    """RAG-specific configuration."""
    datastore_id: str = os.getenv("DATA_STORE_ID", "default")
    datastore_region: str = os.getenv("DATA_STORE_REGION", "us")
    vector_search_index: Optional[str] = os.getenv("VECTOR_SEARCH_INDEX")
    top_k_results: int = int(os.getenv("TOP_K_RESULTS", "5"))


@dataclass
class AgentSettings:
    """Agent configuration."""
    model: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    temperature: float = float(os.getenv("TEMPERATURE", "0.0"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))


@dataclass
class AppSettings:
    """Application settings."""
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    rag: RAGSettings = RAGSettings()
    agent: AgentSettings = AgentSettings()


settings = AppSettings()
```

Usage in your agent:

```python
# app/agent.py
from app.config.settings import settings

root_agent = Agent(
    name="root_agent",
    model=settings.agent.model,
    instruction="You are a helpful assistant.",
    tools=[...],
)
```

### 3. Logging and Observability Pattern

```python
# app/app_utils/logging.py
import logging
import json
from google.cloud import logging as google_cloud_logging

# Set up Google Cloud Logging
logging_client = google_cloud_logging.Client()
cloud_logger = logging_client.logger(__name__)

# Also set up standard Python logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def log_structured(message: str, severity: str = "INFO", **kwargs) -> None:
    """Log structured data to Google Cloud Logging.
    
    Args:
        message: Log message
        severity: Log severity (INFO, WARNING, ERROR, etc.)
        **kwargs: Additional fields to log
    """
    log_entry = {
        "message": message,
        "timestamp": time.time(),
        **kwargs
    }
    cloud_logger.log_struct(log_entry, severity=severity)


def log_tool_call(tool_name: str, input_data: dict, output: str) -> None:
    """Log tool execution for debugging and monitoring."""
    log_structured(
        message=f"Tool execution: {tool_name}",
        severity="INFO",
        tool_name=tool_name,
        input=json.dumps(input_data),
        output=output,
    )
```

### 4. Dependency Injection Pattern

```python
# app/services/service_container.py
from typing import Optional
from app.services.retriever import DocumentRetriever
from app.services.processor import DataProcessor
from app.config.settings import settings


class ServiceContainer:
    """Dependency injection container for services."""
    
    def __init__(self):
        self._retriever: Optional[DocumentRetriever] = None
        self._processor: Optional[DataProcessor] = None
    
    @property
    def retriever(self) -> DocumentRetriever:
        """Lazy-load document retriever."""
        if self._retriever is None:
            self._retriever = DocumentRetriever(
                datastore_id=settings.rag.datastore_id,
                region=settings.rag.datastore_region,
            )
        return self._retriever
    
    @property
    def processor(self) -> DataProcessor:
        """Lazy-load data processor."""
        if self._processor is None:
            self._processor = DataProcessor()
        return self._processor


# Global container
container = ServiceContainer()


# app/tools.py
from app.services.service_container import container


def retrieve_documents(query: str) -> str:
    """Use injected retriever."""
    return container.retriever.retrieve(query)


def process_data(data: str) -> str:
    """Use injected processor."""
    return container.processor.process(data)
```

### 5. Testing Strategy

```python
# tests/conftest.py
import pytest
from google.adk.sessions import InMemorySessionService
from app.agent import root_agent


@pytest.fixture
def session_service():
    """Provide in-memory session service for tests."""
    return InMemorySessionService()


@pytest.fixture
def test_session(session_service):
    """Create a test session."""
    return session_service.create_session_sync(
        user_id="test_user",
        app_name="test"
    )


# tests/integration/test_agent.py
from google.adk.agents.run_config import RunConfig
from google.adk.runners import Runner
from google.genai import types


def test_agent_responds_to_query(session_service, test_session):
    """Test agent can respond to user queries."""
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="test"
    )
    
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Hello, how are you?")]
    )
    
    events = list(
        runner.run(
            new_message=message,
            user_id="test_user",
            session_id=test_session.id,
            run_config=RunConfig(),
        )
    )
    
    assert len(events) > 0
    
    # Verify response contains text
    has_text = False
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    has_text = True
                    break
    
    assert has_text, "Agent should return text response"
```

### 6. Environment Configuration Pattern

```bash
# .env.example
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global

# Agent Configuration
LLM_MODEL=gemini-2.5-flash
TEMPERATURE=0
MAX_TOKENS=2048

# RAG Configuration (if using agentic_rag)
DATA_STORE_ID=your-datastore-id
DATA_STORE_REGION=us
TOP_K_RESULTS=5

# Session Configuration
SESSION_TYPE=in_memory  # or: alloydb, agent_engine
DB_HOST=localhost
DB_USER=postgres
DB_NAME=agent_sessions

# Deployment
DEBUG=false
ALLOW_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 7. Customizing Makefile

```makefile
# Add to Makefile for custom commands
.PHONY: help custom-test deploy-custom

help:
	@echo "Custom Agent Commands:"
	@echo "  make custom-test      - Run custom tests"
	@echo "  make deploy-custom    - Deploy with custom settings"

custom-test:
	uv run pytest tests/ -v --cov=app

deploy-custom:
	@echo "Deploying with custom configuration..."
	gcloud run deploy my-agent \
		--source . \
		--region us-central1 \
		--set-env-vars="CUSTOM_VAR=value"

lint:
	uv run ruff check app/
	uv run mypy app/

format:
	uv run ruff format app/
```

### 8. Documentation Best Practices

```markdown
# API Documentation

## Tools

### retrieve_documents
Retrieve relevant documents from knowledge base.

**Parameters:**
- `query` (string): The search query
- `max_results` (int, default=5): Maximum results to return

**Returns:** Formatted document content

**Example:**
```python
retrieve_documents("How to implement authentication?")
```

### process_data
Process and transform input data.

**Parameters:**
- `data` (string): The data to process

**Returns:** Processed data

**Errors:**
- `ValueError`: If data format is invalid
- `TimeoutError`: If processing takes too long

---

## Agent Configuration

Environment variables control agent behavior:

- `LLM_MODEL`: Model to use (default: gemini-2.5-flash)
- `TEMPERATURE`: LLM temperature (0-1, default: 0)
- `MAX_TOKENS`: Maximum tokens (default: 2048)
```

---

## Summary: Key Customization Patterns

| Pattern | Use Case | Implementation |
|---------|----------|-----------------|
| Remote Templates | Share reusable agent configurations | `pyproject.toml` + Git repository |
| Custom Tools | Add specialized functionality | Python functions with type annotations |
| Multi-Agent Orchestration | Complex task decomposition | CrewAI crews or LangGraph workflows |
| Session Management | User state persistence | AlloyDB, Agent Engine, or in-memory |
| Hierarchical Agents | Team-like collaboration | CrewAI with delegation enabled |
| Conditional Routing | Request classification | LangGraph conditional edges |
| Tool Integration | External service access | Wrapper functions with error handling |
| Caching | Performance optimization | Decorator or service layer |
| Configuration Management | Environment-specific settings | Dataclass with environment variables |
| Testing | Quality assurance | pytest with fixtures and integration tests |

---

## Additional Resources

- **Official Documentation**: https://googlecloudplatform.github.io/agent-starter-pack/
- **ADK Samples**: https://github.com/google/adk-samples
- **Agent Development Kit**: https://github.com/google/adk-python
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **CrewAI Docs**: https://docs.crewai.com/
- **Vertex AI Agents**: https://cloud.google.com/vertex-ai/generative-ai/docs/agents/agent-engine/overview

