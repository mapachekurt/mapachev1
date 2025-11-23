# Mapache v1 - System Architecture

**Version:** 1.0.0
**Last Updated:** 2025-11-17
**Status:** Production-Ready

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Integration Points](#integration-points)
5. [Design Decisions](#design-decisions)
6. [Scalability Considerations](#scalability-considerations)
7. [Technology Stack](#technology-stack)
8. [Module Dependencies](#module-dependencies)
9. [Extension Points](#extension-points)
10. [Architecture Diagrams](#architecture-diagrams)

---

## 1. Overview

### 1.1 Purpose

Mapache v1 is a production-grade, multi-agent system framework built on Google's Agent Development Kit (ADK). It provides a comprehensive infrastructure for deploying, managing, and scaling **1000+ specialized SaaS integration agents** (agents 512-1511) on Google Vertex AI Agent Engine.

### 1.2 High-Level Architecture

The system is architected as a **modular, layered framework** with seven core modules providing orthogonal concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Layer (1000+ Agents)               │
│                    SaaS Integration Agents                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Core Framework Modules                    │
├─────────────────────────────────────────────────────────────┤
│  Evaluation  │  Observability  │  Memory  │  Coordination   │
├──────────────┼─────────────────┼──────────┼─────────────────┤
│  Deployment  │  Optimization   │  Reliability                │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  Google ADK │ Vertex AI │ Cloud Logging │ Cloud Trace       │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Design Philosophy

1. **Zero External Dependencies for Core Features**: Uses in-memory implementations for vector search, message brokerage, and caching to minimize operational complexity
2. **Production-First**: Built with reliability patterns (circuit breakers, retries, timeouts, bulkheads) from the ground up
3. **Horizontal Scalability**: Stateless agent design enables linear scaling to 1000+ agents
4. **Observable by Default**: Structured logging, distributed tracing, and metrics collection are first-class concerns
5. **Progressive Deployment**: Blue-green and canary deployment strategies for zero-downtime releases
6. **Cost Optimization**: Intelligent LLM routing and cost tracking built into the core

### 1.4 Key Characteristics

- **Agent Count**: 1000+ specialized SaaS agents (complete)
- **Concurrency Model**: Fully async using Python asyncio
- **Deployment Target**: Google Vertex AI Agent Engine
- **LLM Model**: Gemini 2.0 Flash Exp (with multi-model routing)
- **Programming Language**: Python 3.10+
- **Architecture Pattern**: ReAct (Reasoning + Acting)
- **State Management**: Hybrid (session + vector memory)

---

## 2. System Components

The framework consists of seven core modules, each providing a distinct set of capabilities:

### 2.1 Evaluation Module (`src/evaluation/`)

**Purpose**: Continuous validation and quality assurance for agent outputs

**Components**:

#### 2.1.1 Golden Task System
```python
# src/evaluation/golden_tasks.py
- GoldenTask: Reference tasks with expected outputs
- AcceptanceCriterion: Validation rules (exact match, contains, regex, numeric, custom)
- GoldenTaskSet: Organized collections of golden tasks
```

**Features**:
- Define reference tasks with acceptance criteria
- Support for multiple validation types (exact, contains, regex, numeric, custom functions)
- Cost constraints per task (max_cost_usd)
- Timeout enforcement (timeout_ms)
- Category-based organization

#### 2.1.2 Task Executor
```python
# src/evaluation/executor.py
- GoldenTaskExecutor: Executes golden tasks and validates outputs
- TaskResult: Individual task execution results
- ExecutionReport: Aggregate metrics across all tasks
```

**Features**:
- Parallel or sequential execution
- Timeout management with asyncio
- Automatic validation against acceptance criteria
- Cost estimation and tracking
- Pass/fail reporting with detailed metrics

#### 2.1.3 Quality Gates
```python
# src/evaluation/quality_gates.py
- QualityGate: Configurable quality thresholds
- GateCheck: Individual gate validation results
- Multiple gate types: pass_rate, avg_latency, max_cost, error_rate
```

**Features**:
- Configurable quality thresholds
- Multi-dimensional quality checks
- Automated deployment blocking on failures
- Historical trend analysis

**Data Flow**:
```
Input Task → Executor → Agent → Output → Validator → Acceptance Check
                                              ↓
                                    TaskResult + Metrics
                                              ↓
                                    Quality Gate Evaluation
                                              ↓
                                    Deploy Decision (Pass/Fail)
```

### 2.2 Observability Module (`src/observability/`)

**Purpose**: Comprehensive monitoring, logging, and tracing for distributed agent systems

**Components**:

#### 2.2.1 Structured Logging
```python
# src/observability/structured_logging.py
- AgentLogger: JSON-formatted structured logging
- Context binding and unbinding
- Integration with structlog (with stdlib fallback)
```

**Features**:
- JSON-formatted logs for machine parsing
- Automatic context injection (agent_id, environment, etc.)
- Log level management (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Performance metrics logging
- Error tracking with stack traces

**Example Output**:
```json
{
  "timestamp": "2025-11-17T10:30:45.123Z",
  "level": "INFO",
  "agent_id": "agent-512",
  "environment": "production",
  "event": "task_completed",
  "task_id": "task-123",
  "duration_ms": 234.5,
  "cost_usd": 0.0042
}
```

#### 2.2.2 Distributed Tracing
```python
# src/observability/distributed_tracing.py
- AgentTracer: OpenTelemetry-based distributed tracing
- Span management for request flows
- Integration with Google Cloud Trace
```

**Features**:
- End-to-end request tracing across agents
- Automatic span creation and propagation
- Latency breakdown by operation
- Parent-child span relationships
- Trace sampling and filtering

#### 2.2.3 Metrics Collection
```python
# src/observability/metrics.py
- AgentMetrics: Real-time metrics collection
- Counter, gauge, histogram support
- Request tracking with automatic timing
```

**Features**:
- Request rate and error rate tracking
- Latency percentiles (p50, p95, p99)
- Token usage and cost metrics
- Custom metric dimensions (agent_id, task_type, etc.)
- Time-series data export

#### 2.2.4 Dashboard Definitions
```python
# src/observability/dashboards.py
- AgentOverviewDashboard: High-level agent health
- AgentPerformanceDashboard: Latency and throughput
- LLMMetricsDashboard: Model usage and costs
- ErrorAnalysisDashboard: Error rates and patterns
```

**Features**:
- Pre-built dashboard configurations for Looker Studio and Grafana
- Automated BigQuery integration for long-term storage
- Real-time alerting on anomalies
- SLO/SLA tracking

**Integration**:
```
Agent Operation
      ↓
Logger.info() → Cloud Logging → BigQuery → Looker Studio
      ↓
Tracer.span() → Cloud Trace → Trace Viewer
      ↓
Metrics.inc() → Cloud Monitoring → Dashboards & Alerts
```

### 2.3 Memory Module (`src/memory/`)

**Purpose**: Multi-tiered memory system for agent state management and knowledge retention

**Components**:

#### 2.3.1 Session Memory (Short-term)
```python
# src/memory/session_memory.py
- Session: Conversation session container
- SessionEntry: Individual interaction record
- SessionMemory: In-memory session management
```

**Features**:
- Conversation history tracking
- Session lifecycle management (create, update, close)
- Entry metadata (timestamp, role, content)
- Session expiration (configurable TTL)
- Multi-session support per agent

**Data Structure**:
```python
Session {
  session_id: str
  agent_id: str
  user_id: Optional[str]
  created_at: datetime
  last_accessed: datetime
  entries: List[SessionEntry]
  metadata: Dict[str, Any]
}
```

#### 2.3.2 Vector Memory (Long-term)
```python
# src/memory/vector_memory.py
- VectorMemory: Semantic search over memories
- MemoryVector: Embedding-enabled memory entry
- SimpleEmbedding: In-memory embedding generation
- SearchResult: Similarity search results
```

**Features**:
- **Zero External Dependencies**: In-memory vector storage and search
- Cosine similarity search for semantic retrieval
- Simple deterministic embeddings (hash + character/word features)
- Importance scoring and access tracking
- Tag-based organization
- Memory consolidation support

**Embedding Strategy**:
```
Text → Normalization → Feature Extraction → Vector (128-dim)
         ↓               ↓
    Lowercase       Char Distribution (32 dims)
    Strip          Word Hashes (32 dims)
                   Statistical Features (32 dims)
                   Structural Features (32 dims)
                        ↓
                   L2 Normalization → Embedding Vector
```

**Search Algorithm**:
1. Generate query embedding
2. Filter by agent_id, tags
3. Calculate cosine similarity with all candidate memories
4. Sort by similarity (descending)
5. Return top-k results with similarity scores

#### 2.3.3 Memory Consolidation
```python
# src/memory/consolidation.py
- MemoryConsolidator: Automated memory pruning
- Importance scoring algorithms
- Redundancy detection
```

**Features**:
- Automatic pruning of low-importance memories
- Redundancy detection and removal
- Importance boost/penalty mechanisms
- Access-based importance adjustment
- Age-based importance decay

**Consolidation Strategies**:
- **Recency-based**: Keep recently accessed memories
- **Importance-based**: Keep high-importance memories
- **Access-based**: Keep frequently accessed memories
- **Hybrid**: Weighted combination of all factors

#### 2.3.4 Memory Patterns
```python
# src/memory/patterns.py
- ExperienceReplayPattern: Learn from past interactions
- DigitalTwinPattern: Maintain agent state snapshots
```

**Features**:
- Experience replay for training and debugging
- Digital twin snapshots for rollback and analysis
- Temporal memory versioning

**Memory Tiers**:
```
┌────────────────────────────────────────┐
│   Session Memory (Short-term)          │
│   - Current conversation context        │
│   - TTL: 1-24 hours                     │
│   - Storage: In-memory                  │
└────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────┐
│   Vector Memory (Long-term)             │
│   - Semantic knowledge base             │
│   - TTL: Days to months                 │
│   - Storage: In-memory (with export)    │
└────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────┐
│   External Storage (Archive)            │
│   - BigQuery / Cloud Storage            │
│   - TTL: Indefinite                     │
│   - Storage: Cloud persistence          │
└────────────────────────────────────────┘
```

### 2.4 Coordination Module (`src/coordination/`)

**Purpose**: Enable multi-agent communication, synchronization, and orchestration

**Components**:

#### 2.4.1 A2A Protocol (Agent-to-Agent)
```python
# src/coordination/a2a_protocol.py
- A2AMessage: Standardized message format
- MessageType: REQUEST, RESPONSE, EVENT, BROADCAST, ERROR
```

**Message Schema**:
```python
A2AMessage {
  message_id: str              # Unique message identifier
  from_agent_id: str          # Sender agent ID
  to_agent_id: Optional[str]  # Recipient (None = broadcast)
  message_type: MessageType   # Message category
  conversation_id: str        # Conversation thread ID
  content: Dict[str, Any]     # Payload
  timestamp: datetime         # Creation time
  metadata: Dict[str, Any]    # Additional context
}
```

#### 2.4.2 Message Broker
```python
# src/coordination/message_broker.py
- MessageBroker: In-memory pub/sub system
- Topic-based subscriptions
- Agent-specific routing
- Dead letter queue
```

**Features**:
- **Publish/Subscribe**: Topic-based message routing
- **Agent Routing**: Direct agent-to-agent messaging
- **Type Filtering**: Subscribe to specific message types
- **Broadcast**: Send to all subscribers
- **Dead Letter Queue**: Failed message handling
- **Message History**: Optional persistence (in-memory)
- **Queue Management**: Configurable max queue sizes

**Routing Logic**:
```
Message Published
      ↓
   Broker
      ↓
┌─────┴─────┬─────────┬──────────┐
│ Topic     │ Agent   │ Type     │ Broadcast
│ Subs      │ Subs    │ Subs     │ Subs
└─────┬─────┴─────────┴──────────┘
      ↓
Queue → Agent Consumers
```

#### 2.4.3 Orchestration Patterns
```python
# src/coordination/orchestration_patterns.py
- OrchestrationPattern: Base pattern interface
- HierarchicalPattern: Manager-worker hierarchy
- PipelinePattern: Sequential processing chain
- PeerToPeerPattern: Collaborative processing
```

**Pattern Details**:

**Hierarchical Pattern**:
```
     Manager Agent
         ↓
    Distribute Tasks
         ↓
   ┌─────┼─────┐
Worker1 Worker2 Worker3
   │     │     │
   └─────┴─────┘
         ↓
   Aggregate Results
```

**Pipeline Pattern**:
```
Input → Agent1 → Agent2 → Agent3 → Output
       (Parse)  (Process) (Format)
```

**Peer-to-Peer Pattern**:
```
Agent1 ←→ Agent2
  ↕         ↕
Agent3 ←→ Agent4
  (Collaborative consensus)
```

#### 2.4.4 Coordination Primitives
```python
# src/coordination/primitives.py
- Semaphore: Concurrent access control
- Barrier: Multi-agent synchronization
- Queue: FIFO message passing
```

**Features**:
- Async-native primitives using asyncio
- Timeout support
- Configurable capacities
- Thread-safe operations

### 2.5 Deployment Module (`src/deployment/`)

**Purpose**: Production deployment strategies with progressive rollout and automated rollback

**Components**:

#### 2.5.1 Blue-Green Deployment
```python
# src/deployment/blue_green.py
- BlueGreenDeployment: Zero-downtime deployment
- DeploymentEnvironment: Environment state tracking
- Traffic switching mechanism
```

**Workflow**:
```
1. Blue (current) serving 100% traffic
2. Deploy Green (new version)
3. Run smoke tests on Green
4. Switch traffic: Blue → Green (atomic)
5. Monitor Green
6. Keep Blue for rollback (configurable retention)
```

**Features**:
- Atomic traffic switching
- Instant rollback capability
- Health check validation
- Resource isolation
- Cost optimization (terminate old environment)

#### 2.5.2 Canary Deployment
```python
# src/deployment/canary.py
- CanaryDeployment: Gradual traffic migration
- TrafficConfig: Traffic split management
- MetricsSnapshot: Performance validation
```

**Workflow**:
```
Traffic Steps: [5%, 10%, 25%, 50%, 100%]

Step 1: 5% canary, 95% stable
         ↓ (validate 30s)
Step 2: 10% canary, 90% stable
         ↓ (validate 30s)
Step 3: 25% canary, 75% stable
         ↓ (validate 30s)
Step 4: 50% canary, 50% stable
         ↓ (validate 30s)
Step 5: 100% canary, 0% stable
         ↓
     Complete
```

**Validation Metrics**:
- Error rate increase < 5%
- Latency increase < 20%
- Success rate decrease < 5%
- CPU/Memory within bounds

**Auto-Rollback Triggers**:
- Metrics degrade beyond thresholds
- Health check failures
- Manual intervention

#### 2.5.3 Rollback Manager
```python
# src/deployment/rollback.py
- RollbackManager: Automated rollback orchestration
- DeploymentSnapshot: Version state capture
- Rollback strategy execution
```

**Features**:
- Automatic rollback on failure detection
- Manual rollback trigger
- Deployment history tracking
- State snapshot management
- Multi-version rollback support

#### 2.5.4 Smoke Tests
```python
# src/deployment/smoke_tests.py
- SmokeTests: Post-deployment validation
- TestSeverity: CRITICAL, HIGH, MEDIUM, LOW
- TestSuite: Organized test collections
```

**Test Categories**:
- **Health Checks**: Endpoint availability
- **Functional Tests**: Core operations
- **Integration Tests**: External dependencies
- **Performance Tests**: Response time validation

**Severity Levels**:
- **CRITICAL**: Deployment blocker (e.g., health endpoint down)
- **HIGH**: Major functionality (e.g., API authentication)
- **MEDIUM**: Secondary features (e.g., cache miss)
- **LOW**: Non-critical warnings (e.g., slow response)

### 2.6 Optimization Module (`src/optimization/`)

**Purpose**: Cost optimization and performance tuning for LLM operations

**Components**:

#### 2.6.1 LLM Router
```python
# src/optimization/llm_router.py
- LLMRouter: Intelligent model selection
- ComplexityLevel: SIMPLE, MODERATE, COMPLEX, EXPERT
- ModelConfig: Model specifications and costs
```

**Routing Strategy**:
```
Request Analysis
      ↓
Complexity Estimation (0-15 points)
  - Prompt length (1-3 points)
  - Context length (1-3 points)
  - Complexity keywords (1-4 points)
  - Code generation (2 points)
  - Multi-step reasoning (2 points)
  - Function calling (2 points)
  - Technical depth (0-4 points)
      ↓
Model Selection
  - SIMPLE (0-2): local-slm ($0)
  - MODERATE (3-5): gpt-3.5-turbo ($0.002/1k)
  - COMPLEX (6-9): gpt-4 ($0.03/1k)
  - EXPERT (10+): gpt-4-turbo ($0.01/1k)
      ↓
Cost-Quality Optimization
```

**Complexity Indicators**:
- **EXPERT**: analyze, evaluate, design, architect, optimize, refactor
- **COMPLEX**: explain, compare, generate code, review, implement
- **MODERATE**: summarize, translate, format, convert, list

**Context Window Handling**:
- Automatic model upgrade if context exceeds max_tokens
- Fallback chain: EXPERT → COMPLEX → MODERATE

#### 2.6.2 Cost Tracker
```python
# src/optimization/cost_tracker.py
- CostTracker: Comprehensive cost monitoring
- CostRecord: Individual cost events
- CostSummary: Aggregated analytics
- BudgetAlert: Budget threshold notifications
```

**Features**:
- **Multi-dimensional Tracking**: agent_id, user_id, task_id, model_name
- **Real-time Cost Calculation**: Token-based pricing
- **Budget Management**: Per-agent, per-user, global budgets
- **Alert System**: 80%, 90%, 100% threshold alerts
- **Cost Analytics**:
  - Top spenders by dimension
  - Cost trends (hourly, daily, weekly)
  - Category breakdowns
  - Model usage patterns

**Cost Categories**:
```python
CostCategory:
  - LLM_API: Language model API calls
  - EMBEDDING: Text embedding generation
  - STORAGE: Vector and session storage
  - COMPUTE: Processing and infrastructure
  - OTHER: Miscellaneous costs
```

**Budget Monitoring**:
```
Record Cost Event
      ↓
Update Aggregates (agent, user, task, global)
      ↓
Check Budget Thresholds
      ↓
Generate Alerts (if threshold exceeded)
      ↓
Send Notifications
```

#### 2.6.3 Caching Layer
```python
# src/optimization/caching.py
- ResponseCache: LLM response caching
- Cache strategies: LRU, TTL-based
- Cache key generation from prompts
```

**Features**:
- Semantic cache key generation
- TTL-based expiration
- LRU eviction policy
- Cache hit/miss metrics
- Configurable cache size

#### 2.6.4 Local SLM Support
```python
# src/optimization/local_slm.py
- LocalSLM: Small language model runner
- Offload simple tasks to local models
- Zero API cost for basic operations
```

**Use Cases**:
- Simple classification
- Basic text formatting
- Keyword extraction
- Regex-based parsing

### 2.7 Reliability Module (`src/reliability/`)

**Purpose**: Fault tolerance and resilience patterns for production systems

**Components**:

#### 2.7.1 Circuit Breaker
```python
# src/reliability/circuit_breaker.py
- CircuitBreaker: Prevent cascading failures
- CircuitState: CLOSED, OPEN, HALF_OPEN
```

**State Machine**:
```
       CLOSED (Normal)
           ↓
    Failures ≥ threshold
           ↓
        OPEN (Blocked)
           ↓
    Timeout elapsed
           ↓
    HALF_OPEN (Testing)
      ↙          ↘
Success        Failure
  ↓              ↓
CLOSED        OPEN
```

**Configuration**:
```python
CircuitBreakerConfig:
  - failure_threshold: 5      # Failures before opening
  - success_threshold: 2      # Successes to close from half-open
  - timeout: 60.0             # Seconds before half-open attempt
  - half_open_max_calls: 1    # Concurrent calls in half-open
```

**Example**:
```python
circuit = CircuitBreaker(failure_threshold=3, timeout=30)

async def call_external_service():
    if circuit.is_open():
        raise CircuitBreakerError("Service unavailable")

    try:
        result = await circuit.call(external_api.request, data)
        return result
    except Exception as e:
        # Circuit automatically records failure
        raise
```

#### 2.7.2 Retry Pattern
```python
# src/reliability/retry.py
- AsyncRetry: Exponential backoff retry
- Retry decorator for async functions
```

**Features**:
- Exponential backoff: delay = base_delay * (2 ** attempt)
- Jitter to prevent thundering herd
- Max retry attempts
- Configurable exception types
- Retry callback hooks

**Configuration**:
```python
@retry(
    max_attempts=5,
    base_delay=1.0,
    max_delay=60.0,
    exponential_base=2,
    jitter=True,
    exceptions=(TimeoutError, ConnectionError)
)
async def flaky_operation():
    # May fail and retry
    pass
```

#### 2.7.3 Timeout Pattern
```python
# src/reliability/timeout.py
- TimeoutManager: Operation timeout enforcement
- wait_for: Async timeout wrapper
```

**Features**:
- Operation-level timeouts
- Graceful timeout handling
- Timeout context manager
- Nested timeout support

**Example**:
```python
async with timeout(seconds=5.0):
    result = await long_running_operation()

# Or as decorator
@timeout(seconds=10.0)
async def operation():
    pass
```

#### 2.7.4 Bulkhead Pattern
```python
# src/reliability/bulkhead.py
- Bulkhead: Resource isolation
- BulkheadRegistry: Manage multiple bulkheads
```

**Purpose**: Isolate resources to prevent resource exhaustion

**Features**:
- Limit concurrent operations per resource
- Queue overflow handling
- Resource pool management
- Prevent resource starvation

**Example**:
```python
# Limit concurrent database connections
db_bulkhead = Bulkhead(max_concurrent=10, max_queue_size=50)

async def query_database():
    async with db_bulkhead:
        result = await db.execute(query)
        return result
```

**Combined Reliability Pattern**:
```python
# Real-world usage combining all patterns
@timeout(seconds=30)
@retry(max_attempts=3, base_delay=1.0)
async def resilient_operation():
    circuit = CircuitBreaker(failure_threshold=5)
    bulkhead = Bulkhead(max_concurrent=10)

    if circuit.is_open():
        raise CircuitBreakerError("Circuit open")

    async with bulkhead:
        result = await circuit.call(external_service.request)
        return result
```

---

## 3. Data Flow

### 3.1 Agent Request Flow

```
1. User Request
      ↓
2. Agent Router (LLMRouter complexity estimation)
      ↓
3. Session Memory (Load conversation context)
      ↓
4. Vector Memory (Semantic search for relevant knowledge)
      ↓
5. LLM Invocation (with selected model)
      ↓
6. Response Generation
      ↓
7. Session Memory (Store interaction)
      ↓
8. Observability (Log, trace, metrics)
      ↓
9. Cost Tracker (Record costs)
      ↓
10. Response to User
```

**Detailed Flow Diagram**:
```
┌────────────────┐
│  User Request  │
└───────┬────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Request Handler                       │
│  - Parse request                       │
│  - Extract context                     │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  LLM Router                            │
│  - Estimate complexity                 │
│  - Select model                        │
│  - Check cache                         │
└───────┬────────────────────────────────┘
        │
        ├─── Cache Hit? ──→ Return Cached Response
        │
        ▼
┌────────────────────────────────────────┐
│  Memory Retrieval (Parallel)           │
│  ┌──────────────┬──────────────┐      │
│  │ Session Mem  │ Vector Mem   │      │
│  │ (Short-term) │ (Long-term)  │      │
│  └──────────────┴──────────────┘      │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Context Assembly                      │
│  - Conversation history                │
│  - Relevant memories                   │
│  - System prompts                      │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Circuit Breaker Check                 │
│  - Is circuit open?                    │
└───────┬────────────────────────────────┘
        │
        ├─── Open? ──→ Fast Fail Error
        │
        ▼
┌────────────────────────────────────────┐
│  Bulkhead Acquire                      │
│  - Check resource availability         │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  LLM API Call (with Retry + Timeout)   │
│  - Retry on transient failures         │
│  - Timeout enforcement                 │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Response Processing                   │
│  - Parse response                      │
│  - Extract structured data             │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Memory Storage (Parallel)             │
│  ┌──────────────┬──────────────┐      │
│  │ Session Mem  │ Vector Mem   │      │
│  │ Update       │ Store New    │      │
│  └──────────────┴──────────────┘      │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Observability (Parallel)              │
│  ┌──────┬───────┬──────────┐          │
│  │ Log  │ Trace │ Metrics  │          │
│  └──────┴───────┴──────────┘          │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────┐
│  Cost Tracking                         │
│  - Record token usage                  │
│  - Calculate cost                      │
│  - Check budgets                       │
└───────┬────────────────────────────────┘
        │
        ▼
┌────────────────┐
│  User Response │
└────────────────┘
```

### 3.2 Multi-Agent Coordination Flow

```
Agent A (Initiator)
      ↓
Create A2AMessage
      ↓
MessageBroker.publish()
      ↓
┌─────┴─────┬─────────┬──────────┐
│           │         │          │
Agent B   Agent C   Agent D   Agent E
│           │         │          │
Subscribe  Subscribe Subscribe Subscribe
│           │         │          │
Process    Process   Process   Process
│           │         │          │
└─────┬─────┴─────────┴──────────┘
      ↓
Aggregate Results (if needed)
      ↓
Response to User
```

### 3.3 Evaluation Flow

```
1. Golden Task Definition
      ↓
2. GoldenTaskExecutor.execute_task()
      ↓
3. Agent Invocation (with timeout)
      ↓
4. Output Validation (AcceptanceCriterion)
      ↓
5. Cost Check (against max_cost_usd)
      ↓
6. TaskResult Generation
      ↓
7. Quality Gate Evaluation
      ↓
8. Deploy Decision (Pass/Fail)
```

### 3.4 Deployment Flow (Canary)

```
1. New Version Ready
      ↓
2. Deploy Canary (5% traffic)
      ↓
3. SmokeTests.run()
      ↓
4. Metrics Collection (30s validation)
      ↓
5. Metrics Validation (error rate, latency, etc.)
      ↓
   Pass? ──→ Yes ──→ Increase Traffic (10%)
      │              ↓
      │          Repeat Steps 4-5
      │              ↓
      │          100% Traffic → Complete
      │
      ▼
   Fail? ──→ Rollback to Stable
      ↓
  Deployment Failed
```

### 3.5 Memory Consolidation Flow

```
Trigger (scheduled or threshold-based)
      ↓
MemoryConsolidator.consolidate()
      ↓
1. Calculate Importance Scores
   - Recency factor
   - Access count factor
   - Explicit importance
      ↓
2. Find Redundant Memories
   - Cosine similarity > threshold
      ↓
3. Apply Pruning Strategy
   - Remove low-importance
   - Remove redundant
   - Keep top N by importance
      ↓
4. Update Memory Store
      ↓
Consolidation Complete
```

---

## 4. Integration Points

### 4.1 Google Cloud Platform Integration

```
┌─────────────────────────────────────────────────────────┐
│              Mapache Framework                          │
└────────┬────────────────────────────────────────────────┘
         │
    ┌────┴────┬────────┬──────────┬──────────┬───────────┐
    │         │        │          │          │           │
    ▼         ▼        ▼          ▼          ▼           ▼
Vertex AI  Cloud   Cloud    BigQuery   Secret  Cloud
Agent      Logging Trace              Manager  Storage
Engine
```

**Integration Details**:

#### 4.1.1 Vertex AI Agent Engine
- **Purpose**: Agent hosting and execution
- **Protocol**: ADK (Agent Development Kit)
- **Model**: Gemini 2.0 Flash Exp
- **API**: REST + gRPC
- **Features**: Auto-scaling, managed infrastructure

#### 4.1.2 Cloud Logging
- **Purpose**: Centralized log aggregation
- **Protocol**: Structured JSON logs
- **API**: Cloud Logging API
- **Features**: Log filtering, search, export to BigQuery

#### 4.1.3 Cloud Trace
- **Purpose**: Distributed tracing
- **Protocol**: OpenTelemetry
- **API**: Cloud Trace API
- **Features**: Latency analysis, dependency mapping

#### 4.1.4 BigQuery
- **Purpose**: Long-term analytics storage
- **Protocol**: SQL interface
- **API**: BigQuery API
- **Features**: Petabyte-scale analytics, ML integration

#### 4.1.5 Secret Manager
- **Purpose**: Secure credential storage
- **Protocol**: REST API
- **API**: Secret Manager API
- **Features**: Automatic rotation, versioning, audit logging

#### 4.1.6 Cloud Storage
- **Purpose**: Memory export/import, snapshots
- **Protocol**: REST API
- **API**: Cloud Storage API
- **Features**: Object versioning, lifecycle management

### 4.2 External Service Integration

```
Mapache Agents
      ↓
┌─────────────────────────────────────┐
│  SaaS Agent Layer (1000 agents)     │
│                                     │
│  ┌─────────┐  ┌─────────┐         │
│  │ GitHub  │  │ Slack   │  ...    │
│  │ Agent   │  │ Agent   │         │
│  └─────────┘  └─────────┘         │
└───────┬─────────────────────────────┘
        │
    ┌───┴───┬────────┬──────────┐
    │       │        │          │
    ▼       ▼        ▼          ▼
 GitHub   Slack   Salesforce  Stripe
   API      API      API        API
```

**Integration Patterns**:
- **API Clients**: Tool-specific API wrappers
- **Authentication**: API keys + OAuth (planned)
- **Rate Limiting**: Respect API limits
- **Error Handling**: Retry with exponential backoff
- **Circuit Breakers**: Prevent cascading failures

### 4.3 Internal Module Dependencies

```
                   ┌──────────────┐
                   │ Agent Layer  │
                   └──────┬───────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
    ┌────────┐      ┌─────────┐     ┌──────────┐
    │ Memory │      │  LLM    │     │Observ-   │
    │        │◄────►│ Router  │────►│ability   │
    └────────┘      └─────────┘     └──────────┘
         │                │                │
         │                ▼                │
         │          ┌─────────┐           │
         └─────────►│  Cost   │◄──────────┘
                    │ Tracker │
                    └─────────┘
                          │
                          ▼
                    ┌──────────┐
                    │Reliability│
                    └──────────┘
```

**Dependency Graph**:
```
Evaluation       → Observability, Memory
Observability    → (no dependencies)
Memory           → (no dependencies)
Coordination     → Memory, Observability
Deployment       → Observability, Evaluation
Optimization     → Observability, Memory
Reliability      → Observability
```

---

## 5. Design Decisions

### 5.1 In-Memory Vector Search

**Decision**: Implement vector search without external vector databases

**Rationale**:
- **Operational Simplicity**: No additional infrastructure to manage
- **Cost**: Zero external database costs
- **Latency**: Local search is faster than network calls
- **Portability**: Works anywhere Python runs
- **Scale**: Sufficient for 1000s of memories per agent

**Trade-offs**:
- Limited to single-machine memory
- No persistence across restarts (requires export/import)
- Less sophisticated than purpose-built vector databases

**Mitigation**:
- Export/import to Cloud Storage for persistence
- Memory consolidation to limit growth
- Future: Optional integration with Vertex AI Vector Search

### 5.2 Async-First Architecture

**Decision**: Use Python asyncio throughout the stack

**Rationale**:
- **Concurrency**: Handle 1000+ agents efficiently
- **I/O Bound**: Most operations are API calls
- **Resource Efficiency**: Single process can handle many agents
- **Cost**: Reduce compute requirements

**Implementation**:
```python
# All core operations are async
async def handle_request(request):
    session = await memory.get_session(request.session_id)
    memories = await vector_memory.search(request.query)
    response = await llm.generate(prompt, context)
    await logger.info("Request completed")
    return response
```

### 5.3 Zero External Dependencies for Core Features

**Decision**: Avoid external services for core functionality

**Rationale**:
- **Reliability**: Fewer points of failure
- **Cost**: Reduce operational expenses
- **Latency**: Local operations are faster
- **Portability**: Deploy anywhere

**Examples**:
- In-memory vector search (not Pinecone/Weaviate)
- In-memory message broker (not RabbitMQ/Kafka)
- In-memory caching (not Redis)
- Simple embeddings (not OpenAI embeddings API)

**When External Services Are Used**:
- Google Cloud Platform (Vertex AI, Cloud Logging, etc.) - part of deployment platform
- SaaS API integrations - core agent purpose

### 5.4 Structured Observability

**Decision**: Structured logging + distributed tracing + metrics from day one

**Rationale**:
- **Production Readiness**: Observable systems are maintainable
- **Debugging**: Trace requests across agents
- **SLO Tracking**: Measure and improve performance
- **Cost Optimization**: Identify expensive operations

**Implementation**:
- JSON-formatted logs for machine parsing
- OpenTelemetry for tracing
- Custom metrics for agent-specific KPIs
- Pre-built dashboards for Looker Studio

### 5.5 Progressive Deployment

**Decision**: Support both blue-green and canary deployments

**Rationale**:
- **Risk Mitigation**: Gradual rollout limits blast radius
- **Rollback Speed**: Blue-green enables instant rollback
- **Metrics Validation**: Canary validates with real traffic
- **Flexibility**: Choose strategy based on change type

**Strategy Selection**:
- **Blue-Green**: Infrastructure changes, major versions
- **Canary**: Feature releases, configuration changes

### 5.6 Cost-First Optimization

**Decision**: Build cost tracking and optimization into the core

**Rationale**:
- **Scale**: 1000+ agents can accumulate significant LLM costs
- **Transparency**: Know where money is spent
- **Optimization**: Route to cheaper models when possible
- **Budget Control**: Prevent cost overruns

**Implementation**:
- LLM router selects cheapest model meeting quality requirements
- Real-time cost tracking per agent/user/task
- Budget alerts at 80%, 90%, 100% thresholds
- Local SLM for zero-cost simple tasks

### 5.7 Reliability Patterns Throughout

**Decision**: Apply circuit breakers, retries, timeouts, and bulkheads consistently

**Rationale**:
- **Fault Tolerance**: External APIs can fail
- **Cascading Failures**: Prevent one failure from taking down the system
- **Resource Protection**: Bulkheads prevent resource exhaustion
- **User Experience**: Graceful degradation better than hard failures

**Application**:
- Circuit breakers on all external API calls
- Retry with exponential backoff on transient errors
- Timeouts on all async operations
- Bulkheads for resource pools (database connections, API clients)

### 5.8 Modular Architecture

**Decision**: Seven independent, composable modules

**Rationale**:
- **Separation of Concerns**: Each module has a single responsibility
- **Testability**: Modules can be tested independently
- **Reusability**: Modules can be used in different combinations
- **Maintainability**: Changes are localized

**Module Boundaries**:
- Each module has a clear public API (`__init__.py` exports)
- Minimal cross-module dependencies
- Modules communicate through well-defined interfaces

### 5.9 Golden Task Evaluation

**Decision**: Use golden tasks for continuous validation

**Rationale**:
- **Quality Assurance**: Ensure agent outputs meet standards
- **Regression Detection**: Catch degradations early
- **Deployment Gates**: Block bad deployments automatically
- **Performance Tracking**: Measure improvements over time

**Implementation**:
- Golden task sets per agent type
- Automated execution in CI/CD
- Quality gates block deployment if pass rate < threshold
- Historical tracking for trend analysis

### 5.10 Multi-Tier Memory

**Decision**: Separate session memory (short-term) and vector memory (long-term)

**Rationale**:
- **Performance**: Session memory is fast, constant-time access
- **Semantics**: Vector memory enables semantic search
- **Lifecycle**: Different retention policies for different data
- **Scale**: Consolidation keeps vector memory bounded

**Access Patterns**:
- Session memory: Append-only, sequential access
- Vector memory: Similarity search, random access

---

## 6. Scalability Considerations

### 6.1 Scaling to 1000+ Agents

**Current Architecture**: Designed for 1000 agents (agents 512-1511)

**Scaling Strategy**:

#### 6.1.1 Horizontal Scaling
```
                  Load Balancer
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Instance 1    Instance 2    Instance 3
    (Agents       (Agents       (Agents
     512-679)      680-847)      848-1511)
```

**Features**:
- **Stateless Agents**: No local state dependencies
- **Session Affinity**: Route user to same instance (optional)
- **Auto-scaling**: Scale based on request rate

#### 6.1.2 Vertical Scaling
```
Per-Instance Capacity:
  - 100-200 agents per instance
  - 4-8 CPU cores
  - 16-32 GB RAM
  - Async I/O for high concurrency
```

#### 6.1.3 Resource Isolation
```
Agent Pool 1 (High Priority)
  └─ Bulkhead: 100 concurrent requests

Agent Pool 2 (Standard Priority)
  └─ Bulkhead: 50 concurrent requests

Agent Pool 3 (Low Priority)
  └─ Bulkhead: 20 concurrent requests
```

### 6.2 Memory Scalability

**Challenge**: Vector memory grows with usage

**Solutions**:

#### 6.2.1 Memory Consolidation
```
Trigger: Every 1 hour or 10,000 memories
Strategy:
  1. Calculate importance scores
  2. Remove memories with importance < 0.3
  3. Keep top 5,000 memories
  4. Export pruned memories to Cloud Storage
```

#### 6.2.2 Sharding
```
Memory Shards by Agent ID:
  Shard 0: Agents 512-679   → VectorMemory instance 0
  Shard 1: Agents 680-847   → VectorMemory instance 1
  Shard 2: Agents 848-1015  → VectorMemory instance 2
  Shard 3: Agents 1016-1183 → VectorMemory instance 3
  Shard 4: Agents 1184-1351 → VectorMemory instance 4
  Shard 5: Agents 1352-1511 → VectorMemory instance 5
```

#### 6.2.3 External Vector Store (Future)
```
For scale > 10,000 agents:
  - Migrate to Vertex AI Vector Search
  - Keep in-memory cache for hot memories
  - Async background sync
```

### 6.3 Message Broker Scalability

**Current**: In-memory MessageBroker

**Limitations**: Single-instance only

**Migration Path**:
```
Phase 1: In-memory (current)
  - 1,000 agents
  - 10,000 messages/sec

Phase 2: Redis Pub/Sub (if needed)
  - 10,000 agents
  - 100,000 messages/sec

Phase 3: Cloud Pub/Sub (future)
  - 100,000+ agents
  - 1,000,000+ messages/sec
```

**Current Design Supports Migration**:
```python
# Interface remains the same
broker = MessageBroker()  # or RedisBroker() or CloudPubSubBroker()
await broker.publish(message)
queue = await broker.subscribe(agent_id)
```

### 6.4 Observability Scalability

**Log Volume**: ~1,000 agents × 10 requests/sec × 5 log entries = 50,000 logs/sec

**Strategy**:

#### 6.4.1 Structured Logging
- JSON format enables efficient parsing
- Fields indexed in Cloud Logging
- Retention policy: 30 days hot, 90 days cold

#### 6.4.2 Sampling
```python
# High-volume agents use sampling
if agent_id in high_volume_agents:
    sample_rate = 0.1  # Log 10% of requests
else:
    sample_rate = 1.0  # Log 100% of requests
```

#### 6.4.3 Aggregation
```python
# Aggregate metrics before export
metrics.increment("requests_total")  # Local counter
# Flush to Cloud Monitoring every 60 seconds
```

### 6.5 Cost Scalability

**Challenge**: LLM costs scale with agent count and usage

**Mitigation**:

#### 6.5.1 Intelligent Routing
```
Request Complexity → Model Selection → Cost

SIMPLE     → local-slm      → $0
MODERATE   → gpt-3.5-turbo  → $0.002/1k tokens
COMPLEX    → gpt-4          → $0.03/1k tokens
EXPERT     → gpt-4-turbo    → $0.01/1k tokens

Estimated Savings: 40-60% compared to gpt-4 for all requests
```

#### 6.5.2 Response Caching
```
Cache Hit Rate: 20-30% for common queries
Cost Savings: $0.03/1k tokens × 30% = $0.009/1k tokens saved
```

#### 6.5.3 Budget Controls
```
Per-Agent Budget: $100/month
Per-User Budget: $1,000/month
Global Budget: $50,000/month

Alert at 80%, 90%, 100% thresholds
Block requests if budget exceeded (configurable)
```

### 6.6 Database Scalability (Future)

**Current**: In-memory only

**Migration Path**:
```
Phase 1: In-memory (current)
  - Fast, simple
  - No persistence

Phase 2: Cloud SQL (if persistence needed)
  - Session metadata
  - Memory indexes
  - Cost tracking

Phase 3: Spanner (if global scale needed)
  - Multi-region
  - Strong consistency
  - Horizontal scaling
```

### 6.7 Rate Limiting

**Prevent Abuse**:
```python
# Per-agent rate limiting
agent_limiter = RateLimiter(
    rate=100,  # 100 requests
    per=60     # per 60 seconds
)

# Per-user rate limiting
user_limiter = RateLimiter(
    rate=1000,  # 1000 requests
    per=3600    # per hour
)
```

### 6.8 Performance Targets

```
Metric                     Target          Measured
────────────────────────────────────────────────────
Request Latency (p50)      < 500ms         TBD
Request Latency (p95)      < 2s            TBD
Request Latency (p99)      < 5s            TBD
Throughput                 1000 req/s      TBD
Agent Availability         99.9%           TBD
Error Rate                 < 0.1%          TBD
Memory per Agent           < 50 MB         TBD
CPU per Agent              < 0.1 core      TBD
Cost per 1M Requests       < $50           TBD
```

---

## 7. Technology Stack

### 7.1 Core Technologies

```
┌──────────────────────────────────────────────────┐
│               Language & Runtime                  │
├──────────────────────────────────────────────────┤
│ Python 3.10+                                     │
│ - Type hints throughout (mypy strict mode)       │
│ - asyncio for concurrency                        │
│ - dataclasses for data structures               │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│               Core Dependencies                   │
├──────────────────────────────────────────────────┤
│ google-adk                 >= 1.15.0, < 2.0.0   │
│ google-cloud-aiplatform    >= 1.118.0, < 2.0.0  │
│ google-cloud-logging       >= 3.12.0, < 4.0.0   │
│ google-cloud-trace         >= 1.11.0, < 2.0.0   │
│ opentelemetry-api          >= 1.20.0, < 2.0.0   │
│ opentelemetry-sdk          >= 1.20.0, < 2.0.0   │
│ opentelemetry-exporter-gcp >= 1.9.0, < 2.0.0    │
│ protobuf                   >= 6.31.1, < 7.0.0   │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│             Development Dependencies              │
├──────────────────────────────────────────────────┤
│ pytest                     >= 8.3.4, < 9.0.0     │
│ pytest-asyncio             >= 0.23.8, < 1.0.0    │
│ ruff                       >= 0.4.6, < 1.0.0     │
│ mypy                       >= 1.15.0, < 2.0.0    │
│ codespell                  >= 2.2.0, < 3.0.0     │
└──────────────────────────────────────────────────┘
```

### 7.2 Python Features Used

```python
# Type Hints (mypy strict mode)
def process_request(request: Request) -> Response:
    pass

# Dataclasses for structured data
from dataclasses import dataclass, field
@dataclass
class MemoryVector:
    memory_id: str
    content: str
    embedding: List[float]

# Async/Await for concurrency
async def handle_request(request: Request) -> Response:
    session = await memory.get_session(request.session_id)
    response = await llm.generate(prompt)
    return response

# Context Managers for resource management
async with timeout(seconds=5):
    result = await operation()

# Enums for type safety
from enum import Enum
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

# Generics for type-safe containers
from typing import TypeVar, Generic, List
T = TypeVar('T')
class Container(Generic[T]):
    def get(self) -> T:
        pass
```

### 7.3 Infrastructure Stack

```
┌──────────────────────────────────────────────────┐
│                   Compute                        │
├──────────────────────────────────────────────────┤
│ Vertex AI Agent Engine                           │
│ - Managed agent hosting                          │
│ - Auto-scaling                                   │
│ - Multi-region deployment                        │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                 Observability                    │
├──────────────────────────────────────────────────┤
│ Cloud Logging        - Centralized logs          │
│ Cloud Trace          - Distributed tracing       │
│ Cloud Monitoring     - Metrics & alerts          │
│ BigQuery             - Analytics storage         │
│ Looker Studio        - Dashboards                │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                   Storage                        │
├──────────────────────────────────────────────────┤
│ Cloud Storage        - Memory exports            │
│ Secret Manager       - API keys                  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                   CI/CD                          │
├──────────────────────────────────────────────────┤
│ GitHub Actions       - Primary CI/CD             │
│ Cloud Build          - Alternative runner        │
│ Terraform            - Infrastructure as Code    │
└──────────────────────────────────────────────────┘
```

### 7.4 Development Tools

```
┌──────────────────────────────────────────────────┐
│              Code Quality                        │
├──────────────────────────────────────────────────┤
│ ruff                 - Linting & formatting      │
│ mypy                 - Static type checking      │
│ codespell            - Spell checking            │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│               Package Management                 │
├──────────────────────────────────────────────────┤
│ uv                   - Fast package manager      │
│ pyproject.toml       - Project configuration    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                  Testing                         │
├──────────────────────────────────────────────────┤
│ pytest               - Unit & integration tests  │
│ pytest-asyncio       - Async test support        │
│ nest-asyncio         - Nested event loop support │
└──────────────────────────────────────────────────┘
```

### 7.5 External APIs

```
┌──────────────────────────────────────────────────┐
│                  LLM Models                      │
├──────────────────────────────────────────────────┤
│ Gemini 2.0 Flash Exp   - Primary model          │
│ GPT-4 Turbo            - Complex tasks (optional)│
│ GPT-3.5 Turbo          - Simple tasks (optional) │
│ Local SLM              - Zero-cost tasks         │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                SaaS Integrations                 │
├──────────────────────────────────────────────────┤
│ 1000+ SaaS platforms via REST APIs               │
│ Authentication: API keys + OAuth (future)        │
└──────────────────────────────────────────────────┘
```

---

## 8. Module Dependencies

### 8.1 Dependency Graph

```
┌─────────────┐
│  Evaluation │──────┐
└─────────────┘      │
                     ▼
              ┌──────────────┐
              │ Observability│◄──────────────┐
              └──────────────┘               │
                     ▲                       │
                     │                       │
┌─────────────┐      │      ┌──────────┐    │
│   Memory    │──────┘      │  Coord   │────┘
└─────────────┘             └──────────┘
       ▲                           ▲
       │                           │
       │    ┌──────────────┐      │
       └────│Optimization  │──────┘
            └──────────────┘
                   ▲
                   │
            ┌──────────────┐
            │ Reliability  │
            └──────────────┘
                   ▲
                   │
            ┌──────────────┐
            │ Deployment   │
            └──────────────┘
```

### 8.2 Module Dependency Matrix

```
                Evaluation  Observ  Memory  Coord  Deploy  Optim  Reliab
─────────────────────────────────────────────────────────────────────────
Evaluation          -         ✓       ✓       -       -       -       -
Observability       -         -       -       -       -       -       -
Memory              -         -       -       -       -       -       -
Coordination        -         ✓       ✓       -       -       -       -
Deployment          ✓         ✓       -       -       -       -       ✓
Optimization        -         ✓       ✓       -       -       -       -
Reliability         -         ✓       -       -       -       -       -

Legend: ✓ = Direct dependency, - = No dependency
```

### 8.3 Import Structure

```python
# Evaluation imports
from observability import get_logger, get_metrics
from memory import SessionMemory, VectorMemory

# Coordination imports
from observability import get_logger
from memory import VectorMemory

# Deployment imports
from evaluation import GoldenTaskExecutor, QualityGate
from observability import get_logger, get_metrics
from reliability import CircuitBreaker, retry

# Optimization imports
from observability import get_logger, get_metrics
from memory import VectorMemory

# Reliability imports
from observability import get_logger
```

### 8.4 Circular Dependency Prevention

**Strategy**: Strict dependency hierarchy

**Rules**:
1. **Observability** has zero dependencies (foundation layer)
2. **Memory** has zero dependencies (data layer)
3. **Reliability** only depends on Observability
4. Higher-level modules depend on lower-level modules
5. No circular imports allowed (enforced by linting)

**Enforcement**:
```bash
# Check for circular imports
python -c "import sys; import importlib; importlib.import_module('src.evaluation')"

# Mypy checks import structure
mypy src/ --strict
```

---

## 9. Extension Points

### 9.1 Custom Validation Functions

```python
# src/evaluation/validator.py

# Built-in validators: exact, contains, regex, numeric
# Add custom validator:

from typing import Any

def custom_json_structure_validator(
    expected: dict,
    actual: Any
) -> bool:
    """Validate JSON structure matches expected schema."""
    if not isinstance(actual, dict):
        return False

    for key, value_type in expected.items():
        if key not in actual:
            return False
        if not isinstance(actual[key], value_type):
            return False

    return True

# Use in AcceptanceCriterion
criterion = AcceptanceCriterion(
    name="response_structure",
    validation_type="custom",
    expected_value={"status": str, "data": dict},
    custom_validator=custom_json_structure_validator
)
```

### 9.2 Custom Orchestration Patterns

```python
# src/coordination/orchestration_patterns.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class OrchestrationPattern(ABC):
    @abstractmethod
    async def execute(
        self,
        task: Dict[str, Any],
        agents: List[str]
    ) -> OrchestrationResult:
        """Execute the orchestration pattern."""
        pass

# Implement custom pattern
class MapReducePattern(OrchestrationPattern):
    """Map-reduce pattern for parallel processing."""

    async def execute(
        self,
        task: Dict[str, Any],
        agents: List[str]
    ) -> OrchestrationResult:
        # Map phase: distribute to all agents
        map_results = await asyncio.gather(*[
            self._invoke_agent(agent, task)
            for agent in agents
        ])

        # Reduce phase: aggregate results
        reduced_result = self._reduce(map_results)

        return OrchestrationResult(
            success=True,
            results=reduced_result,
            metadata={"pattern": "map-reduce"}
        )

    def _reduce(self, results: List[Any]) -> Any:
        """Custom reduce logic."""
        # Implement aggregation
        pass
```

### 9.3 Custom Memory Consolidation Strategies

```python
# src/memory/consolidation.py

from typing import List
from .vector_memory import MemoryVector

class CustomConsolidationStrategy:
    """Custom strategy for memory pruning."""

    def select_memories_to_keep(
        self,
        memories: List[MemoryVector],
        max_memories: int
    ) -> List[MemoryVector]:
        """Select which memories to keep."""

        # Custom logic: keep memories with specific tags
        priority_tags = ["critical", "reference", "learned"]

        priority_memories = [
            m for m in memories
            if any(tag in m.tags for tag in priority_tags)
        ]

        other_memories = [
            m for m in memories
            if m not in priority_memories
        ]

        # Sort others by importance
        other_memories.sort(key=lambda m: m.importance, reverse=True)

        # Combine
        selected = priority_memories + other_memories
        return selected[:max_memories]

# Use custom strategy
consolidator = MemoryConsolidator(
    consolidation_strategy=CustomConsolidationStrategy()
)
```

### 9.4 Custom LLM Models

```python
# src/optimization/llm_router.py

# Add custom model to router
router = LLMRouter()

router.add_model_config(
    complexity_level=ComplexityLevel.COMPLEX,
    config=ModelConfig(
        model_name="claude-3-opus",
        cost_per_1k_tokens=0.015,
        max_tokens=200000,
        temperature=0.7,
        supports_functions=True,
        estimated_quality=0.96
    )
)

# Custom complexity estimation
class CustomComplexityEstimator:
    def estimate(self, prompt: str) -> ComplexityLevel:
        # Custom logic
        if "medical" in prompt.lower():
            return ComplexityLevel.EXPERT
        # ... other rules
        return ComplexityLevel.MODERATE
```

### 9.5 Custom Deployment Strategies

```python
# src/deployment/

from abc import ABC, abstractmethod

class DeploymentStrategy(ABC):
    @abstractmethod
    async def deploy(
        self,
        version: str,
        config: Dict[str, Any]
    ) -> DeploymentResult:
        """Execute deployment."""
        pass

class ShadowDeployment(DeploymentStrategy):
    """Deploy new version but don't route traffic (for testing)."""

    async def deploy(
        self,
        version: str,
        config: Dict[str, Any]
    ) -> DeploymentResult:
        # Deploy new version
        await self._deploy_version(version)

        # Mirror traffic to shadow (no user-facing responses)
        await self._enable_traffic_mirroring(version)

        # Collect metrics for comparison
        metrics = await self._collect_shadow_metrics(duration=300)

        # Validate metrics
        if self._metrics_acceptable(metrics):
            return DeploymentResult(success=True, version=version)
        else:
            await self._teardown_shadow(version)
            return DeploymentResult(success=False, version=version)
```

### 9.6 Custom Dashboard Definitions

```python
# src/observability/dashboards.py

class CustomSecurityDashboard(DashboardDefinition):
    """Dashboard for security metrics."""

    def __init__(self):
        super().__init__(
            name="Security Dashboard",
            description="Security and compliance metrics"
        )

    def get_widgets(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "scorecard",
                "title": "Failed Auth Attempts",
                "query": """
                    SELECT COUNT(*) as failed_auth
                    FROM logs
                    WHERE event = 'auth_failure'
                    AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
                """
            },
            {
                "type": "line_chart",
                "title": "API Key Rotation Status",
                "query": """
                    SELECT
                        DATE(timestamp) as date,
                        SUM(CASE WHEN rotated THEN 1 ELSE 0 END) as rotated_keys,
                        SUM(CASE WHEN NOT rotated THEN 1 ELSE 0 END) as stale_keys
                    FROM api_keys
                    GROUP BY date
                    ORDER BY date DESC
                    LIMIT 30
                """
            }
        ]
```

### 9.7 Custom Message Types

```python
# src/coordination/a2a_protocol.py

# Extend MessageType enum
class CustomMessageType(Enum):
    """Custom message types for domain-specific communication."""

    TASK_DELEGATION = "task_delegation"
    RESOURCE_REQUEST = "resource_request"
    CAPABILITY_ANNOUNCEMENT = "capability_announcement"

# Use in messages
message = A2AMessage(
    from_agent_id="agent-512",
    to_agent_id="agent-513",
    message_type=CustomMessageType.TASK_DELEGATION,
    content={
        "task": "process_invoice",
        "priority": "high",
        "deadline": "2025-11-18T10:00:00Z"
    }
)
```

### 9.8 Plugin Architecture (Future)

```python
# Future: Plugin system for extending agents

from abc import ABC, abstractmethod

class AgentPlugin(ABC):
    """Base class for agent plugins."""

    @abstractmethod
    async def on_request(self, request: Request) -> Request:
        """Pre-process request."""
        pass

    @abstractmethod
    async def on_response(self, response: Response) -> Response:
        """Post-process response."""
        pass

class SentimentAnalysisPlugin(AgentPlugin):
    """Add sentiment analysis to agent responses."""

    async def on_request(self, request: Request) -> Request:
        # Analyze user sentiment
        request.metadata["user_sentiment"] = await self._analyze(request.text)
        return request

    async def on_response(self, response: Response) -> Response:
        # Adjust response tone based on sentiment
        if request.metadata.get("user_sentiment") == "frustrated":
            response.text = self._add_empathy(response.text)
        return response

# Register plugin
agent.register_plugin(SentimentAnalysisPlugin())
```

---

## 10. Architecture Diagrams

### 10.1 System Context Diagram

```
                        ┌─────────────────┐
                        │      Users      │
                        └────────┬────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Load Balancer /      │
                    │   API Gateway          │
                    └────────────┬───────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────┐
│                    Mapache Framework                      │
│  ┌─────────────────────────────────────────────────────┐ │
│  │               Agent Layer (1000+ Agents)            │ │
│  │  - GitHub Agent, Slack Agent, Salesforce Agent...  │ │
│  └─────────────────────────────────────────────────────┘ │
│                           │                               │
│  ┌────────────────────────┴────────────────────────────┐ │
│  │              Core Framework Modules                  │ │
│  │  - Evaluation  - Observability  - Memory            │ │
│  │  - Coordination - Deployment - Optimization         │ │
│  │  - Reliability                                       │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────┬──────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Google Cloud │  │   External   │  │   SaaS       │
│   Platform   │  │     LLM      │  │   APIs       │
│              │  │   Providers  │  │              │
│ - Vertex AI  │  │              │  │ - GitHub     │
│ - Logging    │  │ - OpenAI     │  │ - Slack      │
│ - Trace      │  │ - Anthropic  │  │ - Salesforce │
│ - BigQuery   │  │              │  │ - 1000+ more │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 10.2 Agent Request Flow Diagram

```
┌──────┐
│ User │
└───┬──┘
    │ 1. HTTP Request
    ▼
┌─────────────────────────┐
│   API Gateway           │
└──────────┬──────────────┘
           │ 2. Route to Agent
           ▼
┌────────────────────────────────────────────────────┐
│                  Agent Handler                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ 3. Load Session (Session Memory)             │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 4. Search Knowledge (Vector Memory)          │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 5. Route to Model (LLM Router)               │  │
│  └───────────────┬──────────────────────────────┘  │
│                  │ 6. Check Circuit Breaker         │
│                  ▼                                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 7. Call LLM (with Retry + Timeout)           │  │
│  └───────────────┬──────────────────────────────┘  │
│                  │ 8. Response                      │
│                  ▼                                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 9. Store Interaction (Session Memory)        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 10. Store Knowledge (Vector Memory)          │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 11. Log/Trace/Metrics (Observability)        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ 12. Track Cost (Cost Tracker)                │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────┘
                         │ 13. HTTP Response
                         ▼
                     ┌──────┐
                     │ User │
                     └──────┘
```

### 10.3 Multi-Agent Collaboration Diagram

```
User Request: "Analyze GitHub repo and notify team on Slack"

┌──────────────────────────────────────────────────────────┐
│              Orchestrator Agent                           │
│  - Breaks down task                                       │
│  - Coordinates sub-agents                                 │
│  - Aggregates results                                     │
└─────────────┬────────────────────────────────────────────┘
              │
      ┌───────┴───────┐
      │ Publish Task  │
      └───────┬───────┘
              │
              ▼
    ┌─────────────────────┐
    │   MessageBroker     │
    │   (Topic: "tasks")  │
    └─────────┬───────────┘
              │
    ┌─────────┴─────────┬──────────────┐
    │                   │              │
    ▼                   ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  GitHub     │  │   Slack     │  │  Analytics  │
│   Agent     │  │   Agent     │  │    Agent    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       │ 1. Fetch repo  │ 3. Send msg    │ 2. Analyze
       │    commits     │    to team     │    commit data
       │                │                │
       └────────────────┴────────────────┘
                        │
                        ▼ Results published
              ┌─────────────────────┐
              │   MessageBroker     │
              │ (Topic: "results")  │
              └─────────┬───────────┘
                        │
                        ▼ Subscribe
              ┌─────────────────────┐
              │  Orchestrator Agent │
              │  - Aggregates       │
              │  - Returns to user  │
              └─────────────────────┘
```

### 10.4 Memory Architecture Diagram

```
┌────────────────────────────────────────────────────────┐
│                   Agent                                │
└──────────┬───────────────────────────┬─────────────────┘
           │                           │
           │ Short-term                │ Long-term
           │ (Conversation)            │ (Knowledge)
           ▼                           ▼
┌─────────────────────┐    ┌──────────────────────────┐
│  Session Memory     │    │   Vector Memory          │
│                     │    │                          │
│ Structure:          │    │ Structure:               │
│  - session_id       │    │  - memory_id             │
│  - entries[]        │    │  - content               │
│    - role           │    │  - embedding[128]        │
│    - content        │    │  - importance            │
│    - timestamp      │    │  - tags[]                │
│                     │    │  - access_count          │
│ Storage:            │    │                          │
│  - In-memory dict   │    │ Storage:                 │
│  - TTL: 1-24h       │    │  - In-memory dict        │
│                     │    │  - Cosine similarity     │
│ Operations:         │    │                          │
│  - get_session()    │    │ Operations:              │
│  - add_entry()      │    │  - store()               │
│  - get_entries()    │    │  - search()              │
│                     │    │  - get()                 │
└──────────┬──────────┘    └──────────┬───────────────┘
           │                          │
           │ Export                   │ Export
           ▼                          ▼
┌────────────────────────────────────────────────────────┐
│              Cloud Storage (Persistence)               │
│  - Session archives                                    │
│  - Memory snapshots                                    │
│  - Lifecycle: 90 days                                  │
└────────────────────────────────────────────────────────┘
```

### 10.5 Deployment Pipeline Diagram

```
┌──────────────┐
│ Code Change  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────┐
│   GitHub Actions         │
│   Trigger: Push to main  │
└──────────┬───────────────┘
           │
           ├─ 1. Lint (ruff, mypy, codespell)
           │
           ├─ 2. Unit Tests (pytest)
           │
           ├─ 3. Integration Tests
           │
           ├─ 4. Golden Task Evaluation
           │       └─ Quality Gate Check
           │
           ▼
┌──────────────────────────┐
│  Build Container Image   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Push to Artifact Registry               │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Deploy Strategy Selection               │
│  - Blue-Green: Major versions            │
│  - Canary: Feature releases              │
└──────────┬───────────────────────────────┘
           │
           ├─── Canary Deployment ────┐
           │                          │
           ▼                          ▼
┌──────────────────────┐   ┌─────────────────────┐
│ Canary Deployment    │   │ Blue-Green Deploy   │
│                      │   │                     │
│ 1. Deploy 5%         │   │ 1. Deploy Green     │
│ 2. Validate 30s      │   │ 2. Smoke Tests      │
│ 3. Deploy 10%        │   │ 3. Switch Traffic   │
│ 4. Validate 30s      │   │ 4. Monitor          │
│ 5. Deploy 25%        │   │ 5. Keep Blue for    │
│ 6. Validate 30s      │   │    Rollback (6h)    │
│ 7. Deploy 50%        │   └─────────────────────┘
│ 8. Validate 30s      │
│ 9. Deploy 100%       │
│                      │
│ Auto-Rollback if:    │
│  - Error rate > 5%   │
│  - Latency > 20%     │
│  - Failed smoke test │
└──────────────────────┘
```

### 10.6 Observability Data Flow

```
┌─────────────────────────────────────────────────────┐
│                  Agent Operations                   │
└───┬──────────────────┬──────────────────┬──────────┘
    │                  │                  │
    │ Logs             │ Traces           │ Metrics
    ▼                  ▼                  ▼
┌────────────┐  ┌──────────────┐  ┌──────────────┐
│   Logger   │  │   Tracer     │  │   Metrics    │
│  .info()   │  │  .span()     │  │  .inc()      │
└─────┬──────┘  └──────┬───────┘  └──────┬───────┘
      │                │                  │
      │ JSON           │ OTLP             │ Metrics API
      ▼                ▼                  ▼
┌───────────────────────────────────────────────────┐
│           Google Cloud Platform                   │
│                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────┐│
│  │    Cloud     │  │    Cloud     │  │  Cloud  ││
│  │   Logging    │  │    Trace     │  │  Mon.   ││
│  └──────┬───────┘  └──────┬───────┘  └────┬────┘│
│         │                  │                │     │
│         │ Export           │ Export         │     │
│         ▼                  ▼                │     │
│  ┌──────────────────────────────────┐      │     │
│  │          BigQuery                │      │     │
│  │  - Long-term storage             │      │     │
│  │  - SQL analytics                 │      │     │
│  │  - ML integration                │      │     │
│  └──────────┬───────────────────────┘      │     │
│             │                               │     │
└─────────────┼───────────────────────────────┼─────┘
              │                               │
              ▼                               ▼
    ┌──────────────────┐          ┌──────────────────┐
    │  Looker Studio   │          │    Grafana       │
    │   Dashboards     │          │   Dashboards     │
    └──────────────────┘          └──────────────────┘
              │                               │
              └───────────┬───────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Alerting    │
                  │  - PagerDuty  │
                  │  - Email      │
                  │  - Slack      │
                  └───────────────┘
```

### 10.7 Cost Optimization Flow

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│        LLM Router                       │
│  ┌───────────────────────────────────┐  │
│  │ Complexity Analysis (0-15 points) │  │
│  │  - Prompt length                  │  │
│  │  - Context length                 │  │
│  │  - Keywords                       │  │
│  │  - Code generation                │  │
│  │  - Reasoning depth                │  │
│  │  - Technical depth                │  │
│  └─────────────┬─────────────────────┘  │
│                │                         │
│                ▼                         │
│  ┌────────────────────────────────────┐ │
│  │ Model Selection                    │ │
│  │  0-2  → local-slm     ($0)        │ │
│  │  3-5  → gpt-3.5-turbo ($0.002/1k) │ │
│  │  6-9  → gpt-4         ($0.03/1k)  │ │
│  │  10+  → gpt-4-turbo   ($0.01/1k)  │ │
│  └─────────────┬──────────────────────┘ │
└────────────────┼────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│         Response Cache                 │
│  ┌──────────────────────────────────┐  │
│  │ Cache Key: hash(prompt + context)│  │
│  └─────────────┬────────────────────┘  │
│                │                        │
│                ├─ Hit → Return Cached  │
│                │                        │
│                └─ Miss → Continue      │
└────────────────┼───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│         LLM API Call                   │
│  - Selected model                      │
│  - Token counting                      │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│         Cost Tracker                   │
│  ┌──────────────────────────────────┐  │
│  │ Record Cost Event                │  │
│  │  - agent_id                      │  │
│  │  - user_id                       │  │
│  │  - task_id                       │  │
│  │  - model_name                    │  │
│  │  - tokens_used                   │  │
│  │  - cost_usd                      │  │
│  └─────────────┬────────────────────┘  │
│                │                        │
│                ▼                        │
│  ┌──────────────────────────────────┐  │
│  │ Budget Check                     │  │
│  │  - Agent budget: $100/month      │  │
│  │  - User budget: $1000/month      │  │
│  │  - Global budget: $50k/month     │  │
│  └─────────────┬────────────────────┘  │
│                │                        │
│                ├─ < 80% → Continue     │
│                ├─ 80% → Warning Alert  │
│                ├─ 90% → Critical Alert │
│                └─ 100% → Block (opt.)  │
└────────────────┼───────────────────────┘
                 │
                 ▼
          ┌─────────────┐
          │  Dashboard  │
          │  - Cost by  │
          │    agent    │
          │  - Cost by  │
          │    user     │
          │  - Cost by  │
          │    model    │
          │  - Trends   │
          └─────────────┘
```

### 10.8 Reliability Patterns Interaction

```
Request Flow with All Reliability Patterns

┌──────────────┐
│   Request    │
└──────┬───────┘
       │
       ▼
┌────────────────────────────────┐
│  1. Timeout Wrapper (30s)      │
│     ┌──────────────────────┐   │
│     │ TimeoutManager       │   │
│     └──────────┬───────────┘   │
└────────────────┼────────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│  2. Circuit Breaker Check      │
│     ┌──────────────────────┐   │
│     │ CircuitBreaker       │   │
│     │  State: CLOSED       │   │
│     └──────────┬───────────┘   │
│                │                │
│     OPEN? ─────┴──→ Fast Fail  │
│                                 │
└────────────────┼────────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│  3. Bulkhead Acquire           │
│     ┌──────────────────────┐   │
│     │ Bulkhead             │   │
│     │  Slots: 8/10 used    │   │
│     └──────────┬───────────┘   │
│                │                │
│     Full? ─────┴──→ Queue/Reject
│                                 │
└────────────────┼────────────────┘
                 │
                 ▼
┌────────────────────────────────┐
│  4. Retry Wrapper (3 attempts) │
│     ┌──────────────────────┐   │
│     │ AsyncRetry           │   │
│     │  Backoff: exp        │   │
│     └──────────┬───────────┘   │
└────────────────┼────────────────┘
                 │
                 │ Attempt 1
                 ▼
         ┌───────────────┐
         │  API Call     │
         └───────┬───────┘
                 │
         Success? ─┬─── Yes ──→ Return
                   │
                   └─── No
                        │
                        │ Transient?
                        │
                   ┌────┴────┐
                   │         │
                 Yes        No
                   │         │
              Retry with    Fail
              Backoff       │
                   │         │
              Attempt 2     │
                   │         │
              (repeat)      │
                             │
                             ▼
                   ┌──────────────────┐
                   │ Record Failure   │
                   │  - Circuit       │
                   │  - Metrics       │
                   │  - Logs          │
                   └──────────────────┘
```

---

## Summary

Mapache v1 is a production-ready, multi-agent framework designed for scale, reliability, and cost-efficiency. The architecture emphasizes:

1. **Modularity**: Seven independent modules with clear responsibilities
2. **Scalability**: Designed for 1000+ agents with horizontal scaling
3. **Observability**: Structured logging, distributed tracing, and metrics from day one
4. **Reliability**: Circuit breakers, retries, timeouts, and bulkheads throughout
5. **Cost Optimization**: Intelligent model routing and comprehensive cost tracking
6. **Flexibility**: Multiple deployment strategies and extensive extension points
7. **Simplicity**: Zero external dependencies for core features

The system is built on Google ADK and deploys to Vertex AI Agent Engine, with comprehensive integration with Google Cloud Platform for observability and operations.

---

**Document Version**: 1.0.0
**Framework Version**: 1.0.0
**Agent Count**: 1000 (512-1511)
**Status**: Production-Ready

For implementation details, see individual module documentation in `/home/user/mapachev1/src/`.
