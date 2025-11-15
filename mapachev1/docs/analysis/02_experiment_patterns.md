# Agent Starter Pack: Comprehensive Testing and Experimentation Guide

## Table of Contents

1. [Interactive Playground Overview](#interactive-playground-overview)
2. [ADK Web Command Implementation](#adk-web-command-implementation)
3. [Testing Infrastructure and Patterns](#testing-infrastructure-and-patterns)
4. [Vertex AI Evaluation Framework](#vertex-ai-evaluation-framework)
5. [Load Testing and Performance](#load-testing-and-performance)
6. [Local Testing Workflows with Make](#local-testing-workflows-with-make)
7. [Notebook Patterns for Prototyping](#notebook-patterns-for-prototyping)
8. [CLI and Integration Testing](#cli-and-integration-testing)
9. [Testing Best Practices and Strategies](#testing-best-practices-and-strategies)

---

## Interactive Playground Overview

### What is the Interactive Playground?

The interactive playground is a local development environment that allows rapid iteration on agent logic before deployment. It provides:

- **Real-time chat interface** for testing agent responses
- **Session inspection** and state management
- **Visual tracing** of agent execution
- **Hot-reloading** of agent code changes
- **Message editing and history management**
- **User feedback integration** for A/B testing

### Three Playground Implementations

The Agent Starter Pack supports three different interactive playground implementations based on agent type:

#### 1. ADK Web UI (for ADK Agents)
- **Command**: `adk web`
- **Technology**: ADK's built-in web framework
- **Port**: Default localhost:8501
- **Best For**: ADK-based agents (adk_base, adk_a2a_base, adk_live)
- **Features**: 
  - Interactive chat with session history
  - Visual state inspection
  - Agent trace visualization
  - Eval case creation and testing

#### 2. Streamlit Playground (for Non-ADK Agents)
- **Technology**: Python Streamlit framework
- **Port**: Default localhost:8501
- **Best For**: LangGraph, CrewAI, custom agents
- **Features**:
  - Simple web UI with drag-and-drop file upload
  - Message editing with refresh capability
  - Tool call visualization
  - Chat history management
  - User feedback mechanism (thumbs up/down)

#### 3. React/TypeScript UI (for ADK Live)
- **Technology**: React with TypeScript
- **Port**: localhost:8000
- **Best For**: ADK Live agents (real-time, multimodal)
- **Features**:
  - Real-time audio/video streaming
  - WebSocket communication
  - Webcam integration
  - Transcription preview
  - Audio visualization
  - Side panel for controls

---

## ADK Web Command Implementation

### Core Command Structure

```bash
# Basic usage
adk web /path/to/project_root

# With specific agent discovery
adk web . --port 8501 --reload_agents

# For Agent Engine deployments
uv run python -m app.app_utils.expose_app --mode local --local-agent app.agent.root_agent

# For Cloud Run deployments with ADK
uv run uvicorn app.fast_api_app:app --host localhost --port 8000 --reload
```

### How `adk web` Works

1. **Agent Discovery**: Automatically finds agents in subdirectories with `__init__.py` and `agent.py`
2. **Session Management**: Creates in-memory sessions for testing
3. **Event Streaming**: Streams agent events in real-time to the UI
4. **State Inspection**: Exposes session state for debugging
5. **Hot-Reload**: Watches for code changes and reloads agents

### Makefile Integration

```makefile
# From base_template/Makefile
playground:
    @echo "Starting your agent playground..."
    # For ADK agents
    uv run adk web . --port 8501 --reload_agents
    
    # OR for Streamlit-based agents
    uv sync --extra streamlit
    uv run streamlit run frontend/streamlit_app.py \
        --browser.serverAddress=localhost \
        --server.enableCORS=false \
        --server.enableXsrfProtection=false
    
    # OR for ADK Live agents (FastAPI + React)
    uv run python -m app.app_utils.expose_app \
        --mode local \
        --local-agent app.agent.root_agent
```

### Command Usage Examples

```bash
# Terminal 1: Start the playground
cd my-awesome-agent
make playground

# Or manually for ADK agents
uv run adk web . --port 8501 --reload_agents

# Access the UI
# Open browser to: http://localhost:8501 (ADK/Streamlit)
# Or: http://localhost:8000 (ADK Live)
```

### Playground Features in Detail

#### Session Management
```python
# In ADK web UI, sessions are automatically created
# You can inspect session state in the UI sidebar
session = {
    "id": "generated-uuid",
    "user_id": "my_user",
    "app_name": "my_agent",
    "state": {
        # Session state visible in UI
        "key1": "value1",
        "nested": {"data": "structure"}
    },
    "events": [
        # Full conversation history
        {"author": "user", "content": {...}},
        {"author": "agent_name", "content": {...}},
    ]
}
```

#### Message Editing and Refresh
```python
# Streamlit playground supports message editing
# Users can click "Edit" button on messages and refresh agent responses
def display_message_buttons(message, index, col1, col2, col3):
    with col1:
        st.button(label="✎", key=f"{index}_edit", type="primary")
    if message["type"] == "human":
        with col2:
            st.button(
                label="⟳",
                key=f"{index}_refresh",
                on_click=partial(MessageEditing.refresh_message, st, index, content),
            )
        with col3:
            st.button(
                label="X",
                key=f"{index}_delete",
                on_click=partial(MessageEditing.delete_message, st, index),
            )
```

---

## Testing Infrastructure and Patterns

### Test Directory Structure

```
tests/
├── unit/
│   ├── test_makefile_template.py          # Makefile generation tests
│   └── test_dummy.py                       # Template placeholder
├── integration/
│   ├── test_templated_patterns.py          # Agent template patterns
│   ├── test_makefile_usability.py          # Makefile execution tests
│   ├── test_pipeline_parity.py             # Cloud Build vs GitHub Actions
│   ├── test_agent_directory_functionality.py
│   ├── test_remote_templating.py
│   ├── test_template_linting.py
│   └── utils.py
├── cli/
│   ├── commands/
│   │   ├── test_create.py                  # CLI create command tests
│   │   ├── test_enhance.py
│   │   └── test_list.py
│   └── utils/
│       ├── test_cicd.py
│       ├── test_register_gemini_enterprise.py
│       └── test_remote_template.py
├── cicd/
│   ├── test_e2e_deployment.py
│   ├── test_gemini_enterprise_registration.py
│   └── scripts/
│       ├── delete_service_accounts.py
│       ├── delete_agent_engines.py
│       └── delete_alloydb_clusters.py
├── test_frontend/
│   └── [Frontend-specific tests]
└── fixtures/
    ├── makefile_snapshots/
    │   ├── adk_base_cloud_run.makefile
    │   ├── adk_live_agent_engine.makefile
    │   └── [other template configs]
    └── makefile_hashes.json
```

### PyTest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
pythonpath = [".", "agent_starter_pack/frontends/streamlit", "agent_starter_pack"]
testpaths = ["tests"]
addopts = "-s -v --ignore=tests/integration"
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s - %(levelname)s - %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
```

### Test Execution Commands

```bash
# Run all tests (unit only by default)
make test
uv run pytest tests

# Run specific test categories
uv run pytest tests/unit -v
uv run pytest tests/cli -v
uv run pytest tests/integration/test_templated_patterns.py -v

# Run with coverage
uv run pytest tests --cov=agent_starter_pack --cov-report=html

# Run with specific markers
uv run pytest -m "not slow"
uv run pytest -k "test_agent_stream"

# Integration tests (slow, optional)
uv run pytest tests/integration/test_templated_patterns.py -v
INTEGRATION_TEST=TRUE uv run pytest tests/integration
```

---

## Vertex AI Evaluation Framework

### Overview

The Agent Starter Pack includes comprehensive evaluation patterns using Vertex AI's Gen AI Evaluation service. This enables systematic assessment of agent performance across multiple dimensions.

### Evaluation Dimensions

#### 1. Single Tool Usage Evaluation

```python
# From notebooks: Evaluating if agent uses correct tool for task
from vertexai.preview.evaluation.metrics import TrajectorySingleToolUse

metric = TrajectorySingleToolUse(tool_name="get_product_price")

# This evaluates whether agent uses the specified tool
# regardless of other tools used or order
```

**Use Case**: Verify agent correctly identifies and calls the right tool for specific tasks.

#### 2. Trajectory Evaluation (Tool Sequencing)

```python
# Evaluate multi-step tool sequences
trajectory_metrics = [
    "trajectory_exact_match",          # Same tools in same order
    "trajectory_in_order_match",        # Expected tools in order (extras ok)
    "trajectory_any_order_match",       # All expected tools present (order irrelevant)
    "trajectory_precision",              # Proportion of predicted tools that are expected
    "trajectory_recall",                 # Proportion of expected tools that are predicted
]

# All metrics score 0 or 1 (except precision/recall which range 0-1)
```

**Use Case**: Verify agent follows logical sequence of tool calls.

#### 3. Response Quality Evaluation

```python
from vertexai.preview.evaluation.metrics import PointwiseMetric, PointwiseMetricPromptTemplate

# Built-in metrics
response_metrics = ["safety", "coherence"]

# Custom metrics
criteria = {
    "Follows trajectory": (
        "Evaluate whether agent's response logically follows from "
        "the sequence of actions it took..."
    )
}

pointwise_rating_rubric = {
    "1": "Follows trajectory",
    "0": "Does not follow trajectory",
}

response_follows_trajectory_prompt_template = PointwiseMetricPromptTemplate(
    criteria=criteria,
    rating_rubric=pointwise_rating_rubric,
    input_variables=["prompt", "predicted_trajectory"],
)

custom_metric = PointwiseMetric(
    metric="response_follows_trajectory",
    metric_prompt_template=response_follows_trajectory_prompt_template,
)
```

**Use Case**: Assess final agent response quality and logical coherence.

### Evaluation Dataset Format

```json
{
  "eval_set_id": "weather_bot_eval",
  "eval_cases": [
    {
      "eval_id": "london_weather_query",
      "conversation": [
        {
          "user_content": {"parts": [{"text": "What's the weather in London?"}]},
          "final_response": {"parts": [{"text": "The weather in London is cloudy..."}]},
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "get_weather",
                "args": {"city": "London"}
              }
            ]
          }
        }
      ],
      "session_input": {
        "app_name": "weather_app",
        "user_id": "test_user",
        "state": {}
      }
    }
  ]
}
```

### Running Evaluations

```bash
# CLI method
adk web . 
# Then use the UI to create/run eval cases

# Or direct evaluation
adk eval /path/to/agent_folder /path/to/evalset.json

# Or programmatically in Python
from vertexai.preview.evaluation import EvalTask

eval_task = EvalTask(
    dataset=eval_sample_dataset,
    metrics=trajectory_metrics,
    experiment=EXPERIMENT_NAME,
    output_uri_prefix=BUCKET_URI + "/eval-output",
)

eval_result = eval_task.evaluate(
    runnable=agent_parsed_outcome_sync,
    experiment_run_name="my-eval-run"
)
```

### Notebook-Based Evaluation Workflow

```python
# Complete evaluation example
import json
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import pandas as pd
from vertexai.preview.evaluation import EvalTask
from vertexai.preview.evaluation.metrics import TrajectorySingleToolUse

# Step 1: Define agent
def get_product_price(product_name: str):
    """Get product price"""
    prices = {"smartphone": 500, "shoes": 100, "headphones": 50}
    return prices.get(product_name, "N/A")

agent = Agent(
    name="price_agent",
    model="gemini-2.0-flash",
    instruction="You are a product price lookup assistant.",
    tools=[get_product_price],
)

# Step 2: Create evaluation agent function
async def agent_parsed_outcome(query):
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="test", user_id="user_one", session_id="session_one"
    )
    runner = Runner(agent=agent, app_name="test", session_service=session_service)
    
    content = types.Content(role="user", parts=[types.Part(text=query)])
    events = [event async for event in runner.run_async(
        user_id="user_one",
        session_id="session_one",
        new_message=content
    )]
    
    # Parse output
    return {
        "response": "Agent response",
        "predicted_trajectory": [{"tool_name": "get_product_price", ...}]
    }

# Step 3: Prepare dataset
eval_data = {
    "prompt": [
        "Get price for smartphone",
        "Get price for shoes",
    ],
    "predicted_trajectory": [
        [{"tool_name": "get_product_price", "tool_input": {"product_name": "smartphone"}}],
        [{"tool_name": "get_product_price", "tool_input": {"product_name": "shoes"}}],
    ],
}
dataset = pd.DataFrame(eval_data)

# Step 4: Run evaluation
def agent_sync(prompt):
    return asyncio.run(agent_parsed_outcome(prompt))

metrics = [TrajectorySingleToolUse(tool_name="get_product_price")]

eval_task = EvalTask(
    dataset=dataset,
    metrics=metrics,
    experiment="my-experiment",
    output_uri_prefix="gs://my-bucket/eval",
)

result = eval_task.evaluate(runnable=agent_sync, experiment_run_name="run-1")
```

---

## Load Testing and Performance

### Locust-Based Load Testing

The Agent Starter Pack includes Locust load testing templates for WebSocket and HTTP-based agents.

#### Cloud Run Load Testing

```python
# tests/load_test/load_test.py
import json
import logging
import time
from locust import User, between, task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketUser(User):
    """Simulates users making HTTP requests to Cloud Run agent"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    abstract = True

    @task
    def http_conversation(self) -> None:
        """Test HTTP conversation with agent"""
        start_time = time.time()
        response_count = 0
        exception = None

        try:
            user_id = "load-test-user"
            
            # Create session
            session_url = f"{self.host}/apps/app/users/{user_id}/sessions"
            session_response = self.client.post(
                session_url,
                json={"state": {}},
                name="create_session"
            )
            session_id = session_response.json()["id"]
            
            # Send message
            message_data = {
                "app_name": "app",
                "user_id": user_id,
                "session_id": session_id,
                "new_message": {"role": "user", "parts": [{"text": "Hello agent"}]},
                "streaming": True,
            }
            
            message_response = self.client.post(
                f"{self.host}/run_sse",
                json=message_data,
                stream=True,
                name="send_message"
            )
            
            for line in message_response.iter_lines():
                if line and line.startswith("data: "):
                    response_count += 1
                    
        except Exception as e:
            exception = e
            logger.error(f"Error: {e}")
        finally:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="HTTP",
                name="agent_conversation",
                response_time=total_time,
                response_length=response_count * 100,
                response=None,
                context={},
                exception=exception,
            )
```

#### Agent Engine Load Testing with WebSockets

```python
# tests/load_test/load_test.py (Agent Engine variant)
import json
import logging
import time
from websockets.sync.client import connect
from websockets.exceptions import WebSocketException
from locust import User, between, task

class WebSocketUser(User):
    """Simulates users with WebSocket connections to Agent Engine"""
    
    wait_time = between(1, 3)
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert HTTP URL to WebSocket URL
        if self.host.startswith("https://"):
            self.ws_url = self.host.replace("https://", "wss://", 1) + "/ws"
        elif self.host.startswith("http://"):
            self.ws_url = self.host.replace("http://", "ws://", 1) + "/ws"
        else:
            self.ws_url = self.host + "/ws"

    @task
    def websocket_audio_conversation(self) -> None:
        """Test WebSocket conversation with audio input"""
        start_time = time.time()
        response_count = 0
        exception = None

        try:
            with connect(self.ws_url, open_timeout=10, close_timeout=20) as websocket:
                # Wait for setupComplete
                setup_response = websocket.recv(timeout=10.0)
                setup_data = json.loads(setup_response)
                assert "setupComplete" in setup_data
                logger.info("Received setupComplete")
                
                # Send dummy audio chunk
                dummy_audio = bytes([0] * 1024)
                audio_msg = {
                    "user_id": "load-test-user",
                    "realtimeInput": {
                        "mediaChunks": [{
                            "mimeType": "audio/pcm;rate=16000",
                            "data": dummy_audio.hex(),
                        }]
                    },
                }
                
                websocket.send(json.dumps(audio_msg))
                
                # Receive responses
                while True:
                    try:
                        response = websocket.recv(timeout=5.0)
                        response_data = json.loads(response)
                        response_count += 1
                        
                        # Check for completion
                        if response_data.get("serverContent", {}).get("modelTurn") and \
                           response_data["serverContent"]["modelTurn"].get("endTurn"):
                            break
                    except TimeoutError:
                        break
                        
        except WebSocketException as e:
            exception = e
            logger.error(f"WebSocket error: {e}")
        finally:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(
                request_type="WS",
                name="websocket_conversation",
                response_time=total_time,
                response_length=response_count * 100,
                response=None,
                context={},
                exception=exception,
            )
```

#### Running Load Tests

```bash
# Install locust
pip install locust

# Run load test (CLI)
locust -f tests/load_test/load_test.py \
    -u 10 \
    -r 2 \
    -t 5m \
    -H http://localhost:8000

# Run headless (no UI)
locust -f tests/load_test/load_test.py \
    -u 100 \
    -r 10 \
    --headless \
    -t 10m \
    -H https://my-agent.example.com \
    --csv=load_test_results

# Via make command (if configured in template)
make load-test
```

---

## Local Testing Workflows with Make

### Main Make Targets

```makefile
# tests/integration/test_templated_patterns.py
test:
    uv run pytest tests

test-templated-agents:
    uv run pytest tests/integration/test_templated_patterns.py

test-e2e:
    set -a && . tests/cicd/.env && set +a && uv run pytest tests/cicd/test_e2e_deployment.py -v

generate-lock:
    uv run python -m agent_starter_pack.utils.generate_locks

lint:
    uv sync --dev --extra lint
    uv run ruff check . --config pyproject.toml --diff
    uv run ruff format . --check --config pyproject.toml --diff
    uv run mypy --config-file pyproject.toml ./agent_starter_pack/cli ./tests

lint-templated-agents:
    uv run tests/integration/test_template_linting.py

clean:
    rm -rf target/*

install:
    uv sync --dev --extra lint --frozen
```

### Makefile Template Testing

The Makefile template itself is thoroughly tested to ensure consistency across different agent types and deployment configurations.

```bash
# Test Makefile generation for 9 different configurations
uv run pytest tests/unit/test_makefile_template.py -v

# Test with specific category filters
uv run pytest tests/unit/test_makefile_template.py -v -k "test_makefile_hash"       # Fast
uv run pytest tests/unit/test_makefile_template.py -v -k "test_makefile_snapshot"   # With diffs
uv run pytest tests/unit/test_makefile_template.py -v -k "test_adk_live"           # Specific feature

# Test configurations
TEST_CONFIGURATIONS = {
    "adk_base_cloud_run_no_data": {...},
    "adk_base_agent_engine_no_data": {...},
    "adk_live_cloud_run": {...},
    "adk_live_agent_engine": {...},
    "agentic_rag_cloud_run_vertex_search": {...},
    "agentic_rag_cloud_run_vector_search": {...},
    "langgraph_cloud_run_no_data": {...},
    "agent_with_custom_commands": {...},
    "agent_with_agent_garden": {...},
    "adk_a2a_cloud_run": {...},
    "adk_a2a_agent_engine": {...},
}
```

### Makefile Test Verification

```bash
# Validate Makefile usability across templates
uv run pytest tests/integration/test_makefile_usability.py -v

# What it tests:
# 1. Validates no unrendered Jinja2 placeholders
# 2. Extracts all make targets
# 3. Attempts to execute each target with 2-second timeout
# 4. Differentiates between Makefile errors and missing dependencies
# 5. Reports success/failure for each target
```

### Example: Testing a Templated Agent

```bash
# 1. Generate project from template
uv run python -m agent_starter_pack.cli.main create test-agent \
    --agent adk_base \
    --deployment-target cloud_run \
    --region us-central1 \
    --auto-approve

# 2. Install dependencies
cd test-agent
uv sync --dev --extra lint --frozen

# 3. Run unit tests
uv run pytest tests/unit -v

# 4. Run integration tests
INTEGRATION_TEST=TRUE uv run pytest tests/integration -v

# 5. Lint code
uv run ruff check . --diff
uv run mypy --config-file pyproject.toml ./app ./tests

# 6. Try the playground
make playground
```

---

## Notebook Patterns for Prototyping

### ADK App Testing Notebook

Location: `notebooks/adk_app_testing.ipynb`

**Purpose**: Test agents locally before remote deployment

**Workflow**:

#### 1. Setup Environment

```python
import json
import requests
import vertexai

# Initialize Vertex AI
LOCATION = "us-central1"
client = vertexai.Client(location=LOCATION)
```

#### 2. Remote Testing (Agent Engine)

```python
# Detect agent engine ID from metadata
REASONING_ENGINE_ID = None
try:
    with open("../deployment_metadata.json") as f:
        metadata = json.load(f)
        REASONING_ENGINE_ID = metadata.get("remote_agent_engine_id")
except FileNotFoundError:
    pass

# Get existing agent engine
remote_agent_engine = client.agent_engines.get(name=REASONING_ENGINE_ID)

# Test streaming query
async for event in remote_agent_engine.async_stream_query(
    message="hi!", user_id="test"
):
    print(event)

# Register feedback
remote_agent_engine.register_feedback(
    feedback={
        "score": 5,
        "text": "Great response!",
        "invocation_id": "test-invocation-123",
        "user_id": "test",
    }
)
```

#### 3. Local Testing (ADK)

```python
from app.agent_engine_app import agent_engine

agent_engine.set_up()

# Test locally
async for event in agent_engine.async_stream_query(
    message="hi!", user_id="test"
):
    print(event)
```

#### 4. Cloud Run Testing

```python
# Get authentication token
ID_TOKEN = !gcloud auth print-identity-token -q
SERVICE_URL = "YOUR_CLOUD_RUN_URL"

# Create session
user_id = "test_user_123"
session_data = {"state": {"preferred_language": "English"}}

session_response = requests.post(
    f"{SERVICE_URL}/apps/app/users/{user_id}/sessions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ID_TOKEN[0]}"
    },
    json=session_data
)

session_id = session_response.json()["id"]

# Send message with streaming
message_data = {
    "app_name": "app",
    "user_id": user_id,
    "session_id": session_id,
    "new_message": {"role": "user", "parts": [{"text": "Hello!"}]},
    "streaming": True,
}

message_response = requests.post(
    f"{SERVICE_URL}/run_sse",
    headers={"Authorization": f"Bearer {ID_TOKEN[0]}"},
    json=message_data,
    stream=True
)

for line in message_response.iter_lines():
    if line and line.startswith("data: "):
        event = json.loads(line[6:])
        print(f"Received: {event}")
```

### ADK Agent Evaluation Notebook

Location: `notebooks/evaluating_adk_agent.ipynb`

**Purpose**: Comprehensive agent evaluation with Vertex AI

**Key Components**:

```python
# 1. Build agent
from google.adk.agents import Agent

agent = Agent(
    name="test_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant",
    tools=[...]
)

# 2. Prepare evaluation dataset
eval_data = {
    "prompt": ["Query 1", "Query 2"],
    "predicted_trajectory": [
        [{"tool_name": "tool1", "tool_input": {...}}],
        [{"tool_name": "tool2", "tool_input": {...}}],
    ],
}
eval_dataset = pd.DataFrame(eval_data)

# 3. Run evaluations
from vertexai.preview.evaluation import EvalTask

# Single tool usage
single_tool_eval = EvalTask(
    dataset=eval_dataset,
    metrics=[TrajectorySingleToolUse(tool_name="tool1")],
    experiment="my-experiment",
    output_uri_prefix="gs://bucket/eval",
)

result = single_tool_eval.evaluate(runnable=agent_sync)

# Trajectory evaluation
trajectory_eval = EvalTask(
    dataset=eval_dataset,
    metrics=[
        "trajectory_exact_match",
        "trajectory_precision",
        "trajectory_recall",
    ],
    experiment="my-experiment",
    output_uri_prefix="gs://bucket/eval",
)

result = trajectory_eval.evaluate(runnable=agent_sync)

# Custom metrics
custom_metric = PointwiseMetric(
    metric="my_custom_metric",
    metric_prompt_template=custom_template,
)

custom_eval = EvalTask(
    dataset=eval_dataset,
    metrics=[custom_metric],
    experiment="my-experiment",
    output_uri_prefix="gs://bucket/eval",
)

result = custom_eval.evaluate(runnable=agent_sync)

# 4. Visualize results
display_eval_report(result)
plot_bar_plot(result, title="Evaluation Metrics")
display_dataframe_rows(result.metrics_table, num_rows=5)
```

### Notebook Best Practices

1. **Use Virtual Environment**: Notebooks inherit the same `.venv` created by `uv`
2. **Avoid Hardcoding Paths**: Use relative paths from project root
3. **Test Both Local and Remote**: Include cells for different deployment targets
4. **Document Assumptions**: Clearly state what needs to be set up before running
5. **Make Cells Idempotent**: Cells should work when run in any order
6. **Include Error Handling**: Wrap API calls in try-except
7. **Clean Up Resources**: Delete temporary sessions/artifacts after testing

---

## CLI and Integration Testing

### CLI Command Testing

```python
# tests/cli/commands/test_create.py
from click.testing import CliRunner
from agent_starter_pack.cli.commands.create import create

def test_create_command():
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        result = runner.invoke(create, [
            "my-agent",
            "--agent", "adk_base",
            "--deployment-target", "cloud_run",
            "--auto-approve"
        ])
        
        assert result.exit_code == 0
        assert os.path.exists("my-agent/pyproject.toml")
        assert os.path.exists("my-agent/app/agent.py")
```

### Integration Testing Pattern

```python
# tests/integration/test_templated_patterns.py
import pathlib
import subprocess
from tests.integration.utils import run_command

def test_agent_deployment(agent: str, deployment_target: str):
    """Test agent templates with different deployment targets"""
    
    project_path = pathlib.Path("target") / f"{agent}-{deployment_target}"
    
    # 1. Template the project
    run_command([
        "python", "-m", "agent_starter_pack.cli.main", "create",
        project_name,
        "--agent", agent,
        "--deployment-target", deployment_target,
        "--auto-approve",
        "--skip-checks",
    ], pathlib.Path("target"))
    
    # 2. Verify essential files
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / f"{agent_directory}/agent.py").exists()
    
    # 3. Install dependencies
    run_command([
        "uv", "sync", "--dev", "--extra", "lint", "--frozen"
    ], project_path)
    
    # 4. Run tests
    run_command([
        "uv", "run", "pytest", "tests/unit"
    ], project_path, env={"INTEGRATION_TEST": "TRUE"})
```

### Pipeline Parity Testing

```python
# tests/integration/test_pipeline_parity.py
# Compares Cloud Build and GitHub Actions pipeline configurations

class GeminiPipelineComparator:
    """Compares pipelines using Gemini AI"""
    
    def create_comparison_prompt(self, cb_content, gh_content, pipeline_type):
        """Creates prompt for Gemini to compare two pipeline configs"""
        return f"""
        Compare these two CI/CD pipeline configurations...
        
        Cloud Build: {cb_content}
        GitHub Actions: {gh_content}
        
        Are they functionally equivalent? List any differences.
        """
    
    def compare(self):
        """Uses Gemini to verify pipeline parity"""
        result = self.client.models.generate_content(
            self.create_comparison_prompt(...)
        )
        return json.loads(result.text)
```

---

## Testing Best Practices and Strategies

### Test Levels

#### 1. Unit Tests

**Focus**: Individual functions and components

```python
# tests/unit/test_makefile_template.py
def test_makefile_hash():
    """Verify Makefile content hasn't changed unintentionally"""
    renderer = MakefileRenderer()
    rendered = renderer.render(context)
    
    current_hash = hashlib.sha256(rendered.encode()).hexdigest()
    expected_hash = load_baseline_hash()
    
    assert current_hash == expected_hash
```

**Run**: `make test` or `uv run pytest tests/unit -v`

#### 2. Integration Tests

**Focus**: Multiple components working together

```python
# tests/integration/test_agent_directory_functionality.py
def test_agent_deployment():
    # Create project
    # Install dependencies
    # Run tests
    # Verify artifacts
    pass
```

**Run**: `INTEGRATION_TEST=TRUE uv run pytest tests/integration -v`

#### 3. CLI Tests

**Focus**: Command-line interface correctness

```python
# tests/cli/commands/test_create.py
def test_create_with_options():
    runner = CliRunner()
    result = runner.invoke(create, ["my-agent", "--agent", "adk_base"])
    assert result.exit_code == 0
```

**Run**: `uv run pytest tests/cli -v`

#### 4. E2E Tests

**Focus**: Complete deployment workflows

```bash
# Tests actual cloud deployments
make test-e2e

# Requirements:
# - GCP credentials
# - Active project
# - Sufficient quotas
```

#### 5. Load Tests

**Focus**: Performance and scalability

```bash
# Simulate concurrent user load
locust -f tests/load_test/load_test.py -u 100 -r 10 -t 5m
```

### Linting and Code Quality

```bash
# Format code
uv run ruff format .

# Check code style
uv run ruff check . --diff

# Type checking
uv run mypy --config-file pyproject.toml ./agent_starter_pack

# Spell checking
uv run codespell --skip "uv.lock,.venv"

# All combined
make lint
```

### Test Fixtures and Mocking

```python
# tests/fixtures/
@pytest.fixture
def mock_cwd():
    """Mock current working directory"""
    with patch("pathlib.Path.cwd") as mock:
        mock.return_value = Path("/mock/cwd")
        yield mock

@pytest.fixture
def mock_console():
    """Mock Rich console"""
    with patch("agent_starter_pack.cli.commands.create.console") as mock:
        yield mock

def test_with_mocks(mock_cwd, mock_console):
    # Test with mocked dependencies
    pass
```

### Coverage Reports

```bash
# Generate coverage report
uv run pytest tests --cov=agent_starter_pack --cov-report=html

# View report
open htmlcov/index.html
```

### CI/CD Integration

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: astral-sh/setup-uv@v2
      - run: uv sync --dev --extra lint
      - run: uv run pytest tests/unit -v
      - run: uv run ruff check .
      - run: uv run mypy --config-file pyproject.toml ./agent_starter_pack
```

---

## Summary: Recommended Testing Workflow

### Development Phase

1. **Code Changes**
   ```bash
   # Update agent.py, tools.py, etc.
   ```

2. **Local Testing**
   ```bash
   cd my-agent
   make playground
   # Test manually in UI
   ```

3. **Unit Tests**
   ```bash
   uv run pytest tests/unit -v
   ```

4. **Integration Tests**
   ```bash
   INTEGRATION_TEST=TRUE uv run pytest tests/integration -v
   ```

### Pre-Deployment Phase

5. **Evaluation**
   ```bash
   # In notebook
   # - Run eval cases
   # - Check trajectory
   # - Verify response quality
   ```

6. **Code Quality**
   ```bash
   make lint
   ```

7. **Load Testing** (Optional)
   ```bash
   make load-test
   ```

### Deployment Phase

8. **Cloud Deployment**
   ```bash
   make setup-dev-env
   make deploy
   ```

9. **Remote Testing**
   ```python
   # From notebook
   # Test against deployed agent
   ```

### Post-Deployment

10. **Monitoring**
    - Cloud Trace & Logging
    - BigQuery analytics
    - Looker Studio dashboards

---

## Key Resources

- **ADK Documentation**: Comprehensive guide in `agent_starter_pack/resources/docs/adk-cheatsheet.md`
- **Development Guide**: `docs/guide/development-guide.md`
- **Makefile Template Tests**: `tests/unit/test_makefile_template.py`
- **Example Notebooks**: `agent_starter_pack/agents/*/notebooks/`
- **Load Test Templates**: `agent_starter_pack/deployment_targets/*/tests/load_test/`

