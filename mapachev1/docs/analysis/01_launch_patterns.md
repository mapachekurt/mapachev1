# Agent Starter Pack: Complete Launch Patterns Documentation

## Table of Contents
1. [Overview](#overview)
2. [Available Templates](#available-templates)
3. [Cookiecutter Configuration](#cookiecutter-configuration)
4. [Project Initialization Workflow](#project-initialization-workflow)
5. [Configuration Management](#configuration-management)
6. [Environment Setup Patterns](#environment-setup-patterns)
7. [Template Selection Criteria](#template-selection-criteria)
8. [Directory Structure Standards](#directory-structure-standards)
9. [Deployment Patterns](#deployment-patterns)
10. [Best Practices](#best-practices)

---

## Overview

The Agent Starter Pack is a production-ready Python framework for building GenAI agents on Google Cloud Platform. It provides a complete templating system powered by cookiecutter that generates fully functional agent projects with:

- Pre-built agent templates for different use cases
- Integrated CI/CD pipelines (Google Cloud Build or GitHub Actions)
- Observability and monitoring infrastructure
- Data ingestion pipelines for RAG applications
- Frontend components (Streamlit, React)
- Deployment infrastructure for Cloud Run or Agent Engine
- Development tools and documentation

### Quick Start Command
```bash
uvx agent-starter-pack create my-awesome-agent
```

---

## Available Templates

The Agent Starter Pack provides **6 built-in agent templates**, each designed for specific use cases. Templates are stored in `/agent_starter_pack/agents/` directory.

### 1. **ADK Base** (`adk_base`)

**Description:** A foundational ReAct agent built with Google's Agent Development Kit (ADK)

**Best For:**
- Building simple reasoning agents with tool usage
- Projects requiring LLM step-by-step reasoning
- Quick prototyping of AI agents
- Learning ADK patterns

**Configuration:**
```yaml
description: "A base ReAct agent built with Google's Agent Development Kit (ADK)"
example_question: "What's the weather in San Francisco?"
settings:
  requires_data_ingestion: false
  requires_session: true
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies: ["google-adk>=1.15.0,<2.0.0"]
  tags: ["adk"]
  frontend_type: "None"
```

**Key Features:**
- Session management support for multi-turn conversations
- Works with both Cloud Run and Agent Engine
- No frontend included (API-first design)
- Minimal dependencies for fast deployment

**Deployment Targets:**
- Agent Engine (Vertex AI managed service)
- Cloud Run (serverless containers)

---

### 2. **ADK Agent-to-Agent (A2A)** (`adk_a2a_base`)

**Description:** An ADK ReAct agent with Agent2Agent (A2A) Protocol support for distributed agent communication

**Best For:**
- Multi-agent systems with inter-agent communication
- Building federated agent networks
- Applications requiring agent interoperability
- Enterprise agent orchestration

**Configuration:**
```yaml
description: "A base ReAct agent with Agent2Agent (A2A) Protocol support for distributed agent communication and interoperability"
example_question: "What's the weather in San Francisco?"
settings:
  requires_data_ingestion: false
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies: 
    - "google-adk>=1.16.0,<2.0.0"
    - "a2a-sdk~=0.3.9"
    - "nest-asyncio>=1.6.0,<2.0.0"
  tags: ["adk", "a2a"]
  frontend_type: "None"
```

**Key Features:**
- Full A2A Protocol compliance for agent discovery and communication
- A2A Protocol Inspector included for testing
- Enables agents from different frameworks to communicate
- Complex orchestration support

**Notable Commands:**
```bash
make inspector  # Launch A2A Protocol Inspector for testing
```

---

### 3. **ADK Live (Real-time Multimodal)** (`adk_live`)

**Description:** A real-time multimodal agent powered by Gemini Live API for low-latency voice and video interaction

**Best For:**
- Voice-based conversational agents
- Real-time video processing with AI
- Multimodal interactive applications
- Live streaming integration
- High-frequency user interaction scenarios

**Configuration:**
```yaml
description: "Real-time multimodal agent with ADK and Gemini Live API for low-latency voice and video interaction."
settings:
  requires_data_ingestion: false
  frontend_type: "adk_live_react"
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies:
    - "google-adk>=1.16.0,<2.0.0"
    - "click>=8.0.0,<9.0.0"
    - "uvicorn>=0.18.0,<1.0.0"
    - "fastapi>=0.75.0,<1.0.0"
    - "backoff>=2.0.0,<3.0.0"
  tags: ["adk", "adk_live"]
example_question: "What's the weather in San Francisco?"
```

**Key Features:**
- Integrated React frontend (`adk_live_react`)
- FastAPI backend for real-time communication
- Live API support for streaming interactions
- Built-in UI with audio/video capabilities
- Hot-reload development mode

**Notable Commands:**
```bash
make local-backend       # Start FastAPI server with frontend
make ui                  # Streamlit interface (alternative)
make playground-dev      # Dev mode with hot-reload
make build-frontend      # Build React frontend for production
```

---

### 4. **Agentic RAG** (`agentic_rag`)

**Description:** ADK RAG agent for document retrieval and Q&A with data pipeline integration

**Best For:**
- Document-based question answering
- Semantic search applications
- Knowledge base construction
- Enterprise document management
- Grounded AI responses requiring retrieval

**Configuration:**
```yaml
description: "ADK RAG agent for document retrieval and Q&A. Includes a data pipeline for ingesting and indexing documents into Vertex AI Search or Vector Search."
example_question: "How to save a pandas dataframe to CSV?"
settings:
  requires_data_ingestion: true
  requires_session: true
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies:
    - "google-adk>=1.15.0,<2.0.0"
    - "langchain-google-vertexai~=2.0.7"
    - "langchain~=0.3.24"
    - "langchain-core~=0.3.55"
    - "langchain-community~=0.3.17"
    - "langchain-openai~=0.3.5"
    - "langchain-google-community[vertexaisearch]~=2.0.7"
    - "Jinja2~=3.1.6"
  tags: ["adk"]
  frontend_type: "None"
```

**Key Features:**
- Automatic data ingestion pipeline
- Support for Vertex AI Search and Vector Search
- LangChain integration for RAG workflows
- Jinja2 templating for prompt engineering
- Document embedding and indexing included

**Data Ingestion Datastores:**
- **Vertex AI Search**: Managed serverless document store with Google-quality search
- **Vertex AI Vector Search**: Scalable vector search using ScaNN algorithm

**Workflow:**
```bash
make setup-dev-env   # Initialize datastore resources via Terraform
make data-ingestion  # Run the data pipeline to index documents
make playground      # Test RAG agent
```

---

### 5. **LangGraph ReAct Agent** (`langgraph_base_react`)

**Description:** A ReAct agent implementation using LangGraph framework

**Best For:**
- Projects already using LangChain/LangGraph ecosystem
- Complex agent workflows with graph-based logic
- Tool orchestration and state management
- Multi-step reasoning with visual graph representation
- Integration with LangChain tools and chains

**Configuration:**
```yaml
description: "An agent implementing a base ReAct agent using LangGraph"
settings:
  requires_data_ingestion: false
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies:
    - "langchain-google-vertexai>=2.0.7"
    - "langchain~=0.3.14"
    - "langgraph~=0.6.2"
    - "langchain-community~=0.3.17"
    - "langchain-openai~=0.3.5"
  frontend_type: "streamlit"
example_question: "What's the weather in San Francisco?"
```

**Key Features:**
- Built with LangGraph for advanced control flow
- Streamlit frontend for interactive testing
- Full LangChain ecosystem integration
- Visual graph debugging capabilities
- Complex workflow support

---

### 6. **CrewAI Coding Crew** (`crewai_coding_crew`)

**Description:** A multi-agent system implemented with CrewAI for coding and development tasks

**Best For:**
- Multi-agent collaboration scenarios
- Code generation and analysis
- Technical writing and documentation
- Complex task decomposition
- Agent role-based task assignment

**Configuration:**
```yaml
description: "A multi-agent system implemented with CrewAI created to support coding activities"
settings:
  requires_data_ingestion: false
  deployment_targets: ["agent_engine", "cloud_run"]
  extra_dependencies:
    - "langchain-google-vertexai>=2.0.7"
    - "langchain~=0.3.14"
    - "langchain-community~=0.3.17"
    - "langchain-openai~=0.3.5"
    - "langgraph~=0.6.2"
    - "crewai~=0.152.0"
  frontend_type: "streamlit"
example_question: "How can I implement a function to sort a list in Python?"
```

**Key Features:**
- Multi-agent orchestration via CrewAI
- Role-based agent assignment
- Task decomposition and delegation
- Streamlit UI for monitoring agents
- Built-in tool integrations

---

## Cookiecutter Configuration

The Agent Starter Pack uses **cookiecutter** to generate projects with dynamic templating. When a project is created, a `cookiecutter.json` configuration is generated with the following variables:

### Core Variables

| Variable | Type | Purpose | Example |
|----------|------|---------|---------|
| `project_name` | string | Project directory and package name | `my-awesome-agent` |
| `agent_name` | string | Template/agent type used | `adk_base` |
| `package_version` | string | Starter Pack version | `1.0.0` |
| `agent_description` | string | User-facing description | `A ReAct agent` |
| `agent_directory` | string | Agent code directory name | `app` |
| `deployment_target` | string | Where to deploy | `cloud_run` or `agent_engine` |
| `cicd_runner` | string | CI/CD platform | `google_cloud_build` or `github_actions` |
| `session_type` | string | Session storage method | `in_memory`, `alloydb`, `agent_engine` |
| `frontend_type` | string | UI framework | `streamlit`, `adk_live_react`, or `None` |
| `data_ingestion` | boolean | Include data pipeline | `true` or `false` |
| `datastore_type` | string | Data storage backend | `vertex_ai_search` or `vertex_ai_vector_search` |

### Metadata Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `example_question` | string | Example prompt shown in README |
| `tags` | list | Feature tags (`adk`, `a2a`, `adk_live`) |
| `settings` | object | Template configuration object |
| `extra_dependencies` | list | Additional Python packages |

### Content Injection Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `adk_cheatsheet` | string | Embedded ADK quick reference |
| `llm_txt` | string | Project context for AI tools |

### Copy-Without-Render Patterns

The following file patterns are **not processed by Jinja2** during template generation (to prevent syntax conflicts):

```python
_copy_without_render = [
    "*.ipynb",                    # Jupyter notebooks
    "*.json",                     # JSON files
    "*.tsx", "*.ts",             # TypeScript files
    "*.jsx", "*.js",             # JavaScript files
    "*.css",                      # Stylesheets
    "frontend/**/*",              # All frontend files
    "notebooks/*",                # Notebook directory
    ".git/*",                     # Git directory
    "__pycache__/*",              # Python cache
    ".pytest_cache/*",            # Test cache
    ".venv/*",                    # Virtual environment
    "*templates.py",              # Template Python files
    "Makefile",                   # Makefile (merged separately)
]
```

---

## Project Initialization Workflow

### Step 1: Template Selection

The system discovers available templates by scanning the `agents/` directory for `templateconfig.yaml` files.

**Agent Discovery Process:**
```python
# Built-in agents found in:
# /agent_starter_pack/agents/{agent_name}/.template/templateconfig.yaml

# Priority agents (displayed first):
PRIORITY_AGENTS = [
    "adk_base",
    "adk_a2a_base", 
    "adk_live",
    "agentic_rag",
    "langgraph_base_react",
    # crewai_coding_crew listed second
]
```

**Template Input Methods:**

1. **Interactive Selection** (default):
   ```bash
   agent-starter-pack create my-agent
   # System prompts user to select from available templates
   ```

2. **CLI Argument**:
   ```bash
   agent-starter-pack create my-agent --agent adk_base
   agent-starter-pack create my-agent -a 1  # By number
   ```

3. **Remote Templates** (from Git):
   ```bash
   agent-starter-pack create my-agent --agent https://github.com/user/repo/tree/main/path
   agent-starter-pack create my-agent --agent local@/path/to/template
   agent-starter-pack create my-agent --agent adk@data-science  # From adk-samples
   ```

### Step 2: Configuration Selection

The system prompts for or accepts CLI arguments for:

#### Deployment Target
- **Agent Engine**: Vertex AI managed platform (recommended for simplicity)
- **Cloud Run**: GCP serverless containers (recommended for flexibility)

#### CI/CD Runner (if not in auto-approve mode)
- **Google Cloud Build**: GCP-native CI/CD (default, best for GCP projects)
- **GitHub Actions**: GitHub-native CI/CD (better for GitHub-first workflows)

#### Session Type (only for agents with `requires_session: true` and Cloud Run)
- **in_memory**: Session data stored in process memory (stateless, default)
- **AlloyDB**: PostgreSQL-compatible database for session persistence
- **Agent Engine**: Managed session service (only with Agent Engine)

#### Data Ingestion (for RAG agents or with `--include-data-ingestion`)
- **Vertex AI Search**: For semantic document search
- **Vertex AI Vector Search**: For vector-based similarity search

#### Region
- Default: `us-central1`
- Customizable via `--region` flag

### Step 3: Template Assembly

The templating engine combines multiple components in sequence:

```
1. Copy base_template/ (core infrastructure)
   ↓
2. Apply deployment_targets/{target}/ (deployment-specific config)
   ↓
3. Include data_ingestion/ files (if enabled)
   ↓
4. Copy agent_directory from template (agent code)
   ↓
5. Copy frontend_type files (UI components)
   ↓
6. Run cookiecutter with generated cookiecutter.json
   ↓
7. Overlay remote template files (if using remote template)
   ↓
8. Merge Makefiles with template-specific commands
   ↓
9. Clean up unused conditional directories
   ↓
10. Copy uv.lock for dependency consistency
```

### Step 4: GCP Setup (if not skipped)

If `--skip-checks` is not set:

1. **Verify Credentials**:
   ```bash
   gcloud auth application-default print-access-token
   ```

2. **Confirm Project**:
   - Display current account and project
   - Allow user to change if needed

3. **Enable APIs** (optional):
   - Vertex AI API
   - Cloud Run API
   - Cloud Build API (if using Google Cloud Build)

4. **Set Application Default Credentials**:
   ```bash
   gcloud auth application-default set-quota-project {PROJECT_ID}
   ```

### Step 5: Project Creation

- Creates project directory with all generated files
- Creates backup before in-folder templating
- Displays success message with next steps
- Suggests `make install && make {interactive_command}`

---

## Configuration Management

### Template Configuration Files

#### Built-in Templates: `templateconfig.yaml`

Located in: `/agent_starter_pack/agents/{agent_name}/.template/templateconfig.yaml`

```yaml
# Copyright notice
description: "Human-readable template description"
example_question: "Example user prompt for README"

settings:
  # Infrastructure
  deployment_targets: ["agent_engine", "cloud_run"]
  cicd_runners: ["google_cloud_build", "github_actions"]  # Optional, auto-detected
  
  # Features
  requires_data_ingestion: false    # Prompt for datastore selection
  requires_session: true             # Prompt for session type (Cloud Run only)
  
  # Code Organization
  agent_directory: "app"             # Where agent.py lives (can be overridden)
  
  # UI
  frontend_type: "streamlit"         # or "adk_live_react" or "None"
  
  # Development
  interactive_command: "playground"  # make command to run after creation
  
  # Dependencies
  extra_dependencies:
    - "package>=1.0.0,<2.0.0"
  
  # Categorization
  tags: ["adk", "a2a", "adk_live"]   # Feature tags for filtering
```

#### Remote Templates: `pyproject.toml`

Remote templates use the `[tool.agent-starter-pack]` section:

```toml
[tool.agent-starter-pack]
name = "My Custom Agent"
description = "A specialized agent for my use case"
base_template = "adk_base"  # Required for remote templates

[tool.agent-starter-pack.settings]
deployment_targets = ["cloud_run"]
requires_data_ingestion = false
frontend_type = "streamlit"
tags = ["custom"]
```

### CLI Overrides

All configuration can be overridden via command-line flags:

```bash
agent-starter-pack create my-agent \
  --agent adk_base \
  --deployment-target cloud_run \
  --cicd-runner github_actions \
  --session-type alloydb \
  --frontend-type streamlit \
  --include-data-ingestion \
  --datastore vertex_ai_search \
  --region us-west1 \
  --agent-directory myagent \
  --base-template adk_base
```

### Generated Project Configuration

After creation, projects have configuration in:

1. **`pyproject.toml`**: Python dependencies and project metadata
2. **`Makefile`**: Development and deployment commands
3. **`deployment/terraform/`**: Infrastructure-as-code
4. **`GEMINI.md`**: AI assistant context file

---

## Environment Setup Patterns

### Development Environment Setup

```bash
# 1. Install dependencies
make install

# 2. Set up GCP resources (Terraform)
export PROJECT_ID=your-project-id
make setup-dev-env

# 3. For RAG agents: Run data ingestion
make data-ingestion

# 4. Start local development
make playground  # or make local-backend for Cloud Run
```

### Environment Variables

**Standard GCP Setup:**
```bash
export PROJECT_ID=<your-gcp-project-id>
export REGION=us-central1
export GOOGLE_APPLICATION_CREDENTIALS=<path-to-service-account-key>
```

**ADK Live (Optional):**
```bash
# Use Google AI Studio instead of Vertex AI
export VERTEXAI=false
export GOOGLE_API_KEY=<your-api-key>
```

### Development vs. Production Setup

**Dev Environment** (via `terraform/dev/`):
- Minimal resources for testing
- Lower cost configuration
- No production-grade security

**Staging Environment** (CI/CD triggered):
- Intermediate testing environment
- Production-like configuration
- PR check validation

**Production Environment** (via `terraform/prod/`):
- High-availability setup
- Security hardening
- Monitoring and observability
- Automated backups

---

## Template Selection Criteria

### Decision Matrix

| Use Case | Recommended Template | Reasoning |
|----------|---------------------|-----------|
| Simple tool-using agent | `adk_base` | Minimal, focused on reasoning |
| Multi-agent collaboration | `crewai_coding_crew` | Built for agent teams |
| Document Q&A | `agentic_rag` | Built-in data pipeline |
| Voice/Video interaction | `adk_live` | Real-time Gemini Live API |
| LangChain ecosystem | `langgraph_base_react` | Native LangGraph integration |
| Agent networks | `adk_a2a_base` | A2A Protocol support |

### Deployment Target Selection

**Choose Agent Engine if:**
- You want managed, serverless deployment
- Simple agent deployment and scaling
- Built-in authentication and monitoring
- Preference for Vertex AI ecosystem

**Choose Cloud Run if:**
- You need more control over runtime
- Custom middleware or libraries needed
- Existing Cloud Run infrastructure
- More flexibility required

### Frontend Type Selection

**Choose `None` if:**
- Building API-only services
- Frontend built separately
- Integration into larger systems

**Choose `streamlit` if:**
- Quick prototyping needed
- Data scientist-friendly interface
- Python-first development

**Choose `adk_live_react` if:**
- Real-time interaction needed
- Voice/video capabilities required
- Native React frontend desired
- Modern web app experience

---

## Directory Structure Standards

### Base Template Structure

```
{{cookiecutter.project_name}}/
├── {{cookiecutter.agent_directory}}/           # Agent implementation
│   ├── agent.py                  # Main agent logic (ADK/LangGraph)
│   ├── fast_api_app.py           # FastAPI backend (Cloud Run only)
│   ├── agent_engine_app.py       # Agent Engine app (Agent Engine only)
│   └── app_utils/                # Utility modules
│       ├── deploy.py             # Deployment helpers
│       ├── agent_tools.py        # Tool definitions
│       └── llm_helpers.py        # LLM utilities
│
├── frontend/                      # UI components
│   ├── streamlit_app.py          # Streamlit entry point
│   ├── components/               # Reusable UI components
│   ├── utils/                    # Frontend utilities
│   └── package.json              # Frontend dependencies (React)
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_getting_started.ipynb  # Quick start
│   ├── 02_agent_development.ipynb # Agent building guide
│   └── 03_evaluation.ipynb       # Agent evaluation
│
├── tests/                        # Automated tests
│   ├── unit/                     # Unit tests
│   │   └── test_*.py
│   ├── integration/              # Integration tests
│   │   └── test_*.py
│   └── load_test/               # Load/stress tests
│
├── deployment/                   # Infrastructure
│   ├── README.md                # Deployment guide
│   └── terraform/               # Terraform configurations
│       ├── main.tf              # Main infrastructure
│       ├── variables.tf         # Input variables
│       ├── outputs.tf           # Output values
│       ├── dev/                 # Development environment
│       │   ├── terraform.tfvars
│       │   └── service.tf       # Service-specific config
│       └── prod/                # Production environment
│           ├── terraform.tfvars
│           └── service.tf
│
├── data_ingestion/              # RAG data pipeline (if enabled)
│   ├── README.md               # Pipeline documentation
│   ├── data_ingestion_pipeline/ # Pipeline code
│   │   ├── main.py             # Pipeline entry point
│   │   ├── config.py           # Pipeline configuration
│   │   └── submit_pipeline.py  # Vertex AI Pipelines submission
│   └── uv.lock                 # Dependency lock
│
├── .cloudbuild/                 # Google Cloud Build configs (if selected)
│   ├── pr_checks.yaml          # PR validation
│   ├── staging.yaml            # Staging deployment
│   └── deploy-to-prod.yaml     # Production deployment
│
├── .github/                     # GitHub Actions configs (if selected)
│   └── workflows/
│       ├── pr_checks.yaml      # PR validation
│       ├── staging.yaml        # Staging deployment
│       └── deploy-to-prod.yaml # Production deployment
│
├── Makefile                     # Development commands
├── pyproject.toml              # Python dependencies
├── uv.lock                     # Dependency lock file
├── README.md                   # Project documentation
├── GEMINI.md                   # AI assistant context
└── .gitignore                  # Git ignore rules
```

### Agent Code Directory Structure

```
{{cookiecutter.agent_directory}}/
├── agent.py                  # Main agent implementation
├── agent_engine_app.py       # Agent Engine integration (Agent Engine)
├── fast_api_app.py          # FastAPI integration (Cloud Run)
├── app_utils/               # Utility modules
│   ├── __init__.py
│   ├── deploy.py            # Deployment utilities
│   ├── agent_tools.py       # Tool definitions
│   ├── llm_helpers.py       # LLM interaction helpers
│   └── observability.py     # Logging and monitoring
└── __init__.py
```

### Template Subdirectory (`.template/`)

Each agent template has a `.template/` directory:

```
agents/adk_base/.template/
├── templateconfig.yaml       # Template configuration
├── {{cookiecutter.agent_directory}}/
│   ├── agent.py             # Agent template code
│   └── app_utils/
├── deployment/
│   └── terraform/           # Deployment configs
├── tests/                   # Test templates
└── notebooks/              # Example notebooks
```

---

## Deployment Patterns

### Deployment Targets

#### 1. Agent Engine (Vertex AI)

**Description:** Managed platform for deploying AI agents

**How it works:**
- No container management required
- Automatic scaling and monitoring
- Built-in authentication via IAM
- Simplified deployment with `make deploy`

**Configuration:**
```bash
--deployment-target agent_engine
```

**Deployment Command:**
```bash
export PROJECT_ID=your-project-id
make deploy
```

**Generated Files:**
- `deployment/terraform/main.tf` - Agent Engine resource definitions
- `app/agent_engine_app.py` - Endpoint implementation
- `.cloudbuild/deploy-to-prod.yaml` - Cloud Build pipeline
- `.github/workflows/deploy-to-prod.yaml` - GitHub Actions workflow

**After Deployment:**
- Check `latest_deployment_metadata.json` for Engine ID and endpoints
- Query agent via REST API
- Integration with Gemini Enterprise (optional via `make register-gemini-enterprise`)

#### 2. Cloud Run

**Description:** Serverless container execution on GCP

**How it works:**
- Deploy as containerized application
- Full control over runtime environment
- Custom middleware and authentication
- Pay-per-request pricing

**Configuration:**
```bash
--deployment-target cloud_run
```

**Session Options (Cloud Run only):**
```bash
--session-type in_memory       # Stateless (default)
--session-type alloydb        # Persistent database
```

**Deployment Command:**
```bash
export PROJECT_ID=your-project-id
make deploy
# Optional: make deploy IAP=true  # Enable Identity-Aware Proxy
```

**Generated Files:**
- `Dockerfile` - Container specification
- `deployment/terraform/service.tf` - Cloud Run service config
- `app/fast_api_app.py` - FastAPI backend
- `deployment/terraform/dev/service.tf` - Dev environment config
- CI/CD pipeline configurations

**Session Management:**
- **In-memory**: Sessions lost on container restart (stateless)
- **AlloyDB**: Persistent PostgreSQL-compatible sessions
- Automatic session cleanup and garbage collection

### CI/CD Patterns

#### Google Cloud Build

**Triggered by:**
- Push to main branch → production deployment
- Push to staging branch → staging deployment
- Pull requests → validation checks

**Pipeline Structure:**
```yaml
# .cloudbuild/pr_checks.yaml
steps:
  - name: "gcr.io/cloud-builders/gke-deploy"
    args: ["lint", "--..."]

# .cloudbuild/staging.yaml
steps:
  - name: "gcr.io/cloud-builders/gke-deploy"
    args: ["apply", "--..."]

# .cloudbuild/deploy-to-prod.yaml
steps:
  - name: "gcr.io/cloud-builders/gke-deploy"
    args: ["apply", "--..."]
```

**Configuration Locations:**
- YAML files: `.cloudbuild/{pr_checks,staging,deploy-to-prod}.yaml`
- Terraform: `deployment/terraform/{dev,prod}/`
- Service account: `deployment/terraform/service.tf`

#### GitHub Actions

**Triggered by:**
- Push to main branch → production deployment
- Push to staging branch → staging deployment
- Pull requests → validation checks

**Workflow Structure:**
```yaml
# .github/workflows/pr_checks.yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/auth@v1
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}

# .github/workflows/deploy-to-prod.yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/auth@v1
      - uses: google-github-actions/setup-gcloud@v1
```

**Features:**
- Workload Identity Federation (WIF) for secure authentication
- No long-lived credentials needed
- OIDC tokens from GitHub
- Automatic secret rotation

### Infrastructure Setup

**One-Command Setup (Recommended):**
```bash
uvx agent-starter-pack setup-cicd
```

This single command:
1. Sets up GitHub repository configuration
2. Configures Workload Identity Federation
3. Creates service accounts
4. Deploys Terraform infrastructure
5. Sets up CI/CD pipelines

**Manual Setup:**
```bash
cd deployment
export PROJECT_ID=your-project-id
export REGION=us-central1
terraform init
terraform plan
terraform apply
```

---

## Best Practices

### 1. Project Initialization

**DO:**
```bash
# Use uv for consistency
uvx agent-starter-pack create my-agent

# Use auto-approve mode for automation
agent-starter-pack create my-agent \
  --agent adk_base \
  --deployment-target cloud_run \
  --auto-approve

# Normalize project names
agent-starter-pack create my-awesome-agent  # ✓ becomes my-awesome-agent
```

**DON'T:**
```bash
# Avoid special characters and uppercase
agent-starter-pack create My_Awesome_Agent  # Will be normalized

# Avoid names > 26 characters (GCP resource limits)
agent-starter-pack create extremely-long-agent-name-exceeding-limit

# Don't mix local and remote templates without understanding base_template
agent-starter-pack create my-agent --agent https://repo.com/path \
  --base-template adk_base  # Only needed for remote templates
```

### 2. Template Selection

**For Rapid Prototyping:**
```bash
agent-starter-pack create my-agent --agent adk_base
# Minimal dependencies, quick iteration
```

**For Production RAG Systems:**
```bash
agent-starter-pack create my-agent --agent agentic_rag \
  --datastore vertex_ai_search
# Includes data pipeline and LangChain RAG patterns
```

**For Voice/Video Agents:**
```bash
agent-starter-pack create my-agent --agent adk_live
# Real-time Gemini Live API with React frontend
```

**For Multi-Agent Systems:**
```bash
agent-starter-pack create my-agent --agent crewai_coding_crew
# Built-in agent orchestration patterns
```

### 3. Deployment Strategy

**Development → Staging → Production:**
```bash
# 1. Develop locally
make install
make playground

# 2. Test in dev environment
export PROJECT_ID=dev-project
make setup-dev-env
make deploy

# 3. Create CI/CD pipeline (one-time)
uvx agent-starter-pack setup-cicd

# 4. Deploy to production (via Git)
git push main  # Triggers production deployment automatically
```

### 4. Configuration Management

**Use CLI Arguments for Automation:**
```bash
# CI/CD pipeline
agent-starter-pack create my-agent \
  --agent adk_base \
  --deployment-target cloud_run \
  --cicd-runner github_actions \
  --auto-approve
```

**Use Interactive Mode for Manual Setup:**
```bash
agent-starter-pack create my-agent
# System will prompt for each configuration option
```

### 5. Agent Code Organization

**Recommended Structure:**
```
app/
├── agent.py              # Core agent logic only
├── agent_engine_app.py   # Deployment integration
├── fast_api_app.py       # API layer
└── app_utils/
    ├── tools.py          # Tool definitions
    ├── prompts.py        # Prompt templates
    ├── models.py         # Data models
    └── helpers.py        # Utility functions
```

**DO:**
```python
# agent.py - Keep focused on agent logic
from google.adk.client import adk_client
from app.app_utils.tools import get_weather_tool

@adk_client.tool
def weather(location: str) -> str:
    return f"Sunny in {location}"

agent = adk_client.agent(tools=[weather_tool])
```

**DON'T:**
```python
# Don't mix concerns in agent.py
import requests  # HTTP library
import pandas as pd  # Data processing
import asyncio  # Async logic

# Move these to app_utils/
```

### 6. Data Ingestion Best Practices

**For RAG Projects:**
```bash
# 1. Set up infrastructure first
export PROJECT_ID=your-project
make setup-dev-env

# 2. Prepare your data
# Place documents in data_ingestion/documents/

# 3. Run pipeline
make data-ingestion

# 4. Test retrieval
make playground
```

**Data Format Support:**
- PDF files
- Text files
- Markdown documents
- Web pages (via URLs)

**Index Strategy:**
- Use Vertex AI Search for semantic search
- Use Vector Search for similarity matching
- Consider document size and count

### 7. Monitoring and Observability

**Built-in Observability:**
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=my-agent"

# View traces
gcloud trace list

# Access Looker Studio dashboard
# https://lookerstudio.google.com/...
```

**Key Metrics:**
- Request latency and throughput
- Token usage and costs
- Tool call success rates
- Error rates and types

### 8. Version Management

**Dependency Management:**
```bash
# Use uv (modern Python package manager)
uv add package>=1.0.0,<2.0.0

# Update all dependencies
uv sync

# Lock file maintained automatically
# Commit uv.lock to version control
```

**Starter Pack Updates:**
```bash
# Update to latest version
uv add agent-starter-pack@latest

# Update in existing project
uvx agent-starter-pack --version  # Check version
```

### 9. Remote Template Development

**Creating Custom Templates:**

Template projects should have:
```
my-template/
├── pyproject.toml              # Must include [tool.agent-starter-pack]
├── .template/                  # Template code
│   └── {{ agent-specific code }}
├── README.md                   # Documentation
└── .gitignore
```

**Registration:**
```toml
[tool.agent-starter-pack]
name = "My Custom Agent"
description = "Custom implementation"
base_template = "adk_base"

[tool.agent-starter-pack.settings]
deployment_targets = ["cloud_run"]
tags = ["custom"]
frontend_type = "streamlit"
```

### 10. Common Pitfalls to Avoid

**Pitfall 1: Exceeding Project Name Length**
```bash
# ✗ Too long (>26 chars)
agent-starter-pack create my-incredibly-long-agent-name

# ✓ Acceptable
agent-starter-pack create my-long-agent
```

**Pitfall 2: Using Hyphens in Agent Directory**
```bash
# ✗ Invalid (agent_directory cannot contain hyphens)
--agent-directory my-agent

# ✓ Valid
--agent-directory my_agent
```

**Pitfall 3: Forgetting Project Setup**
```bash
# ✗ Skip infrastructure setup
agent-starter-pack create my-agent
make deploy  # Will fail without setup-dev-env

# ✓ Complete setup
agent-starter-pack create my-agent
make setup-dev-env
make deploy
```

**Pitfall 4: Not Setting PROJECT_ID**
```bash
# ✗ Missing environment variable
make setup-dev-env  # Will fail

# ✓ Proper setup
export PROJECT_ID=my-gcp-project
make setup-dev-env
```

**Pitfall 5: Mixing Session Types with Agent Engine**
```bash
# ✗ Invalid combination
--deployment-target agent_engine --session-type alloydb  # Fails

# ✓ Valid combinations
--deployment-target cloud_run --session-type alloydb
--deployment-target agent_engine  # No session-type needed
```

---

## Summary: Launch Patterns by Use Case

### Scenario 1: Build a Simple Chatbot

```bash
# Interactive setup
uvx agent-starter-pack create my-chatbot

# Select: adk_base, Cloud Run, GitHub Actions, Streamlit, in_memory sessions

# Or automated:
uvx agent-starter-pack create my-chatbot \
  --agent adk_base \
  --deployment-target cloud_run \
  --cicd-runner github_actions \
  --auto-approve

# Start developing
cd my-chatbot
make install
make playground
```

### Scenario 2: Deploy RAG System with Documents

```bash
# Create RAG agent
uvx agent-starter-pack create my-rag-system \
  --agent agentic_rag \
  --deployment-target cloud_run \
  --datastore vertex_ai_search \
  --auto-approve

# Setup infrastructure
export PROJECT_ID=my-project
make setup-dev-env

# Ingest documents
make data-ingestion

# Test locally
make playground

# Deploy
make deploy
```

### Scenario 3: Multi-Agent Collaboration

```bash
# Create multi-agent system
uvx agent-starter-pack create my-crew \
  --agent crewai_coding_crew \
  --deployment-target agent_engine \
  --cicd-runner google_cloud_build \
  --auto-approve

# Setup and test
export PROJECT_ID=my-project
make install
make playground
make deploy
```

### Scenario 4: Real-Time Voice Agent

```bash
# Create live multimodal agent
uvx agent-starter-pack create my-voice-agent \
  --agent adk_live \
  --deployment-target agent_engine \
  --auto-approve

# Develop
make install
make local-backend

# Build for production
make build-frontend
make deploy
```

---

## Conclusion

The Agent Starter Pack provides a comprehensive, production-ready framework for AI agent development on Google Cloud. By understanding these launch patterns, configuration options, and best practices, you can quickly scaffold, develop, test, and deploy sophisticated AI agents tailored to your specific use case.

Start with the simplest appropriate template, iterate locally, and use the built-in CI/CD infrastructure for seamless production deployment.

