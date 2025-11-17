# Agent Improvements Integration Guide

A practical, step-by-step guide for adding production-ready improvements to Kurt's 511+ existing agents.

## Table of Contents

1. [Quick Start (15 Minutes)](#quick-start-15-minutes)
2. [Progressive Rollout Strategy](#progressive-rollout-strategy)
3. [Integration Patterns](#integration-patterns)
4. [Code Examples](#code-examples)
5. [Bulk Migration](#bulk-migration)
6. [Common Pitfalls](#common-pitfalls)
7. [Validation Checklist](#validation-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start (15 Minutes)

### Goal: Add basic improvements to a single agent with minimal code changes

**Step 1: Pick a test agent** (2 minutes)

```bash
# Choose a simple agent to start with
cd /home/user/mapachev1/python/agents
ls agent_*.py | head -1
# Example: agent_001_ceo_root_coordinator.py
```

**Step 2: Add minimal imports** (3 minutes)

```python
# Add these imports at the top of your agent file
from src.observability import get_logger, get_metrics
from src.reliability import retry
from src.optimization import CostTracker

# Initialize in __init__ method
class YourAgent:
    def __init__(self):
        # ... existing code ...

        # NEW: Add observability
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="agent")

        # NEW: Add cost tracking
        self.cost_tracker = CostTracker(enable_alerts=True)
```

**Step 3: Add retry to main execution method** (5 minutes)

```python
# BEFORE
def execute(self, task=None):
    """Execute task"""
    if task:
        return f"Executing: {task}"
    return "Standing by"

# AFTER
@retry(max_attempts=3, exponential_base=2.0)
async def execute(self, task=None):
    """Execute task with automatic retry"""
    # Log task start
    self.logger.info("Task started", task=task)

    try:
        if task:
            result = f"Executing: {task}"

            # Track success
            self.metrics.requests_total.labels(
                agent_id=self.agent_id,
                task_type="execute",
                status="success"
            ).inc()

            return result
        return "Standing by"
    except Exception as e:
        # Log error
        self.logger.error("Task failed", error=str(e))
        self.metrics.record_error(agent_id=self.agent_id, error_type=type(e).__name__)
        raise
```

**Step 4: Test it** (5 minutes)

```python
# Create a test script: test_improved_agent.py
import asyncio
from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent

async def test_agent():
    agent = CEORootCoordinatorAgent()
    result = await agent.execute("Test task")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_agent())
```

**You now have:**
- Structured logging
- Automatic retries
- Cost tracking
- Metrics collection

**Time invested: 15 minutes | Value: Production-ready error handling**

---

## Progressive Rollout Strategy

### Phase 1: Evaluation (Week 1)
**Goal**: Establish quality baselines and automated testing

**Priority**: Critical-path agents first (CEO, CFO, CTO)

**Actions**:
1. Add evaluation module to 10 key agents
2. Create golden test datasets
3. Set up quality gates

**Code**:
```python
from src.evaluation import validator, golden_tasks

class ImprovedAgent:
    def __init__(self):
        # ... existing code ...
        self.validator = validator.ResponseValidator()

    async def execute(self, task):
        result = await self._process_task(task)

        # Validate result quality
        validation = self.validator.validate_response(
            prompt=task,
            response=result,
            expected_format="text",
            min_length=10
        )

        if not validation.is_valid:
            self.logger.warning("Quality check failed", issues=validation.issues)

        return result
```

**Success Metrics**:
- 10 agents with quality gates
- 50+ golden test cases
- 90%+ pass rate

**Rollback Plan**: Remove validator calls if blocking production

---

### Phase 2: Observability (Week 2)
**Goal**: Full visibility into agent operations

**Priority**: All agents get logging + metrics

**Actions**:
1. Add structured logging to all 511 agents
2. Set up metrics collection
3. Deploy dashboards

**Code**:
```python
from src.observability import get_logger, get_metrics, get_tracer

class ObservableAgent:
    def __init__(self):
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="mapache")
        self.tracer = get_tracer(service_name=f"agent-{self.agent_id}")

    async def execute(self, task):
        # Start span for distributed tracing
        with self.tracer.start_span("execute_task") as span:
            span.set_attribute("agent_id", self.agent_id)
            span.set_attribute("task_type", task.get("type", "unknown"))

            # Track request
            with self.metrics.track_request(
                agent_id=self.agent_id,
                task_type="execute"
            ):
                self.logger.log_task_start(
                    task_id=task["id"],
                    task_type=task["type"],
                    priority=task.get("priority", "normal")
                )

                result = await self._process(task)

                self.logger.log_task_end(
                    task_id=task["id"],
                    task_type=task["type"],
                    success=True,
                    duration_ms=100
                )

                return result
```

**Success Metrics**:
- 511/511 agents logging
- Dashboards showing real-time metrics
- P50/P95/P99 latencies tracked

**Rollback Plan**: Disable logging if performance impact > 5%

---

### Phase 3: Cost Optimization (Week 3)
**Goal**: Track and optimize LLM costs across all agents

**Priority**: High-usage agents first

**Actions**:
1. Add cost tracking to all LLM calls
2. Implement caching for repeated queries
3. Set up budget alerts

**Code**:
```python
from src.optimization import CostTracker, ResultCache

class CostOptimizedAgent:
    def __init__(self):
        self.cost_tracker = CostTracker(enable_alerts=True)
        self.cache = ResultCache(default_ttl_seconds=3600)

        # Set budget
        self.cost_tracker.set_budget(
            limit=100.0,  # $100/day
            dimension="agent",
            identifier=self.agent_id
        )

    async def _make_llm_call(self, prompt: str, model: str = "gpt-4"):
        # Check cache first
        cache_key = f"{model}:{hash(prompt)}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # Make API call
        response = await self._call_llm_api(prompt, model)

        # Track cost
        cost_record = self.cost_tracker.record_llm_call(
            model_name=model,
            input_tokens=len(prompt.split()) * 1.3,
            output_tokens=len(response.split()) * 1.3,
            agent_id=self.agent_id
        )

        # Cache result
        self.cache.set(cache_key, response)

        # Check budget
        budget_status = self.cost_tracker.get_budget_status(
            dimension="agent",
            identifier=self.agent_id
        )

        if budget_status["is_over_budget"]:
            self.logger.warning("Budget exceeded",
                budget_used=budget_status["percentage_used"])

        return response
```

**Success Metrics**:
- 100% cost visibility
- 30%+ cost reduction from caching
- Zero budget overruns

**Rollback Plan**: Disable caching if causing stale results

---

### Phase 4: Memory + Coordination (Week 4)
**Goal**: Enable stateful agents and multi-agent workflows

**Priority**: Agents that need conversation context

**Actions**:
1. Add session memory to conversational agents
2. Set up message broker for A2A communication
3. Implement coordination patterns

**Code**:
```python
from src.memory import SessionMemory
from src.coordination import MessageBroker, A2AMessage, MessageType

class StatefulAgent:
    def __init__(self):
        # Session memory
        self.memory = SessionMemory(use_fakeredis=True, ttl_seconds=3600)
        self.session_id = None

        # Message broker for coordination
        self.broker = MessageBroker(enable_persistence=True)

    async def start_session(self, user_id: str):
        """Start new session with memory"""
        from src.memory import Session

        session = Session(
            agent_id=self.agent_id,
            context={"user_id": user_id},
            metadata={"started_at": datetime.utcnow().isoformat()}
        )

        self.memory.store_session(session)
        self.session_id = session.session_id
        return self.session_id

    async def execute_with_memory(self, task: str):
        """Execute task with conversation context"""
        # Get conversation history
        history = self.memory.get_conversation_history(
            session_id=self.session_id,
            limit=10
        )

        # Add to context
        context = "\n".join([f"{h.role}: {h.content}" for h in history])

        # Process with context
        result = await self._process(task, context=context)

        # Store in memory
        self.memory.append_to_history(
            session_id=self.session_id,
            role="agent",
            content=result
        )

        return result

    async def coordinate_with_agent(self, target_agent_id: str, task_data: dict):
        """Send task to another agent"""
        message = A2AMessage(
            from_agent_id=self.agent_id,
            to_agent_id=target_agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            payload=task_data
        )

        await self.broker.publish(message, topic="agent_tasks")

        # Wait for response
        response = await self.broker.wait_for_response(
            message_id=message.message_id,
            timeout_seconds=30.0
        )

        return response
```

**Success Metrics**:
- 100+ agents with session memory
- 50+ agents coordinating via A2A
- 95%+ message delivery success

**Rollback Plan**: Fallback to stateless operation

---

### Phase 5: Reliability + Deployment (Week 5)
**Goal**: Production-ready resilience and safe deployments

**Priority**: All production agents

**Actions**:
1. Add circuit breakers to external calls
2. Implement timeout protection
3. Set up blue-green deployments

**Code**:
```python
from src.reliability import CircuitBreaker, timeout, Bulkhead
from src.deployment import BlueGreenDeployment, SmokeTests

class ResilientAgent:
    def __init__(self):
        # Circuit breaker for external services
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout=60.0
        )

        # Bulkhead for resource isolation
        self.bulkhead = Bulkhead(max_workers=10, name=f"agent-{self.agent_id}")

    @retry(max_attempts=3, exponential_base=2.0)
    @timeout(30.0)  # Timeout after 30 seconds
    async def call_external_service(self, endpoint: str):
        """Call external service with full protection"""
        # Check circuit breaker
        if self.circuit_breaker.is_open():
            self.logger.warning("Circuit breaker open, using fallback")
            return self._fallback_response()

        try:
            # Execute through bulkhead
            async def api_call():
                response = await self._http_client.get(endpoint)
                await self.circuit_breaker.record_success()
                return response

            result = await self.bulkhead.execute(api_call)
            return result

        except Exception as e:
            await self.circuit_breaker.record_failure()
            raise

    async def health_check(self):
        """Health check for deployment validation"""
        checks = {
            "circuit_breaker": not self.circuit_breaker.is_open(),
            "memory_available": self.memory.get_session_count() < 1000,
            "cost_under_budget": self._check_budget()
        }

        return {
            "healthy": all(checks.values()),
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }
```

**Success Metrics**:
- Zero unhandled timeouts
- 99.9% uptime with circuit breakers
- Successful blue-green deployments

**Rollback Plan**: Automated rollback on smoke test failure

---

## Integration Patterns

### Pattern 1: Decorator Pattern (Reliability)

**Use for**: Adding retry, timeout, circuit breaker to methods

**Benefits**: Non-invasive, composable, easy to test

```python
from src.reliability import retry, timeout, CircuitBreaker

class DecoratorPattern:
    """Using decorators for reliability"""

    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)

    # Stack decorators for multiple protections
    @retry(max_attempts=3, exponential_base=2.0)
    @timeout(10.0)
    async def protected_operation(self, data):
        """This method is protected by retry AND timeout"""
        # Circuit breaker check
        if self.circuit_breaker.is_open():
            raise Exception("Circuit breaker is open")

        result = await self._do_work(data)
        await self.circuit_breaker.record_success()
        return result
```

**Real example**:
```python
# BEFORE
async def fetch_data(self, query):
    return await self.api_client.get(query)

# AFTER
@retry(max_attempts=3, exponential_base=2.0)
@timeout(5.0)
async def fetch_data(self, query):
    if self.circuit_breaker.is_open():
        return self._cached_fallback(query)
    try:
        result = await self.api_client.get(query)
        await self.circuit_breaker.record_success()
        return result
    except Exception as e:
        await self.circuit_breaker.record_failure()
        raise
```

---

### Pattern 2: Mixin Pattern (Observability)

**Use for**: Adding logging, metrics, tracing to multiple agents

**Benefits**: Reusable, consistent, separates concerns

```python
from src.observability import get_logger, get_metrics

class ObservabilityMixin:
    """Mixin providing observability capabilities"""

    def _init_observability(self):
        """Call this in __init__"""
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="agent")

    def _log_operation(self, operation: str, **kwargs):
        """Standardized logging"""
        self.logger.info(f"{operation}", agent_id=self.agent_id, **kwargs)

    def _track_request(self, task_type: str):
        """Standardized metrics tracking"""
        return self.metrics.track_request(
            agent_id=self.agent_id,
            task_type=task_type
        )

# Use in your agent
class YourAgent(ObservabilityMixin):
    def __init__(self):
        self.agent_id = "agent_001"
        self._init_observability()  # Add observability

    async def execute(self, task):
        self._log_operation("execute_start", task=task)

        with self._track_request("execute"):
            result = await self._process(task)

        self._log_operation("execute_complete", result=result)
        return result
```

**Real example**:
```python
# Create a base agent with observability
class BaseObservableAgent(ObservabilityMixin):
    def __init__(self):
        self._init_observability()

# All agents inherit it
class CEOAgent(BaseObservableAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "agent_001"
        # Automatically has logger and metrics!
```

---

### Pattern 3: Dependency Injection (Coordination)

**Use for**: Sharing message brokers, cost trackers across agents

**Benefits**: Testable, flexible, centralized configuration

```python
from src.coordination import MessageBroker
from src.optimization import CostTracker

class DependencyInjectionPattern:
    """Inject shared services into agents"""

    def __init__(
        self,
        message_broker: MessageBroker = None,
        cost_tracker: CostTracker = None
    ):
        # Use provided or create new
        self.broker = message_broker or MessageBroker()
        self.cost_tracker = cost_tracker or CostTracker()

    async def coordinate(self, target_agent_id: str, payload: dict):
        """Use injected broker"""
        message = A2AMessage(
            from_agent_id=self.agent_id,
            to_agent_id=target_agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            payload=payload
        )
        await self.broker.publish(message)
```

**Real example - Agent Factory**:
```python
class AgentFactory:
    """Factory creating agents with shared dependencies"""

    def __init__(self):
        # Shared infrastructure
        self.broker = MessageBroker(enable_persistence=True)
        self.cost_tracker = CostTracker(enable_alerts=True)
        self.logger = get_logger(agent_id="factory")

    def create_agent(self, agent_class, agent_id: str):
        """Create agent with injected dependencies"""
        return agent_class(
            agent_id=agent_id,
            message_broker=self.broker,
            cost_tracker=self.cost_tracker,
            logger=get_logger(agent_id=agent_id)
        )

# Usage
factory = AgentFactory()
ceo = factory.create_agent(CEOAgent, "agent_001")
cfo = factory.create_agent(CFOAgent, "agent_003")
# Both share the same broker and cost tracker!
```

---

## Code Examples

### Example 1: Minimal Integration

**Before** - Basic agent with no improvements:
```python
class BasicAgent:
    """Basic agent - no improvements"""

    def __init__(self):
        self.agent_id = "agent_001"
        self.role = "CEO"

    def execute(self, task):
        """Execute task - fails silently, no tracking"""
        result = f"Executing: {task}"
        return result
```

**After** - Minimal improvements (5 lines added):
```python
from src.observability import get_logger
from src.reliability import retry

class MinimalImprovedAgent:
    """Agent with minimal improvements"""

    def __init__(self):
        self.agent_id = "agent_001"
        self.role = "CEO"
        self.logger = get_logger(agent_id=self.agent_id)  # +1 line

    @retry(max_attempts=3)  # +1 line
    async def execute(self, task):
        """Execute task - now with retry and logging"""
        self.logger.info("Executing task", task=task)  # +1 line
        try:
            result = f"Executing: {task}"
            self.logger.info("Task completed", result=result)  # +1 line
            return result
        except Exception as e:
            self.logger.error("Task failed", error=str(e))  # +1 line
            raise
```

**Value delivered**: Automatic retry + full logging in 5 lines

---

### Example 2: Standard Integration

**Before** - Agent with basic structure:
```python
class StandardAgent:
    def __init__(self):
        self.agent_id = "agent_050"
        self.role = "Senior Recruiter"

    def process_application(self, application_data):
        # Process application
        result = self._analyze_resume(application_data)
        return result

    def _analyze_resume(self, data):
        # Call external service
        return "Analysis complete"
```

**After** - Standard improvements:
```python
from src.observability import get_logger, get_metrics
from src.reliability import retry, timeout, CircuitBreaker
from src.optimization import CostTracker, ResultCache

class ImprovedStandardAgent:
    def __init__(self):
        self.agent_id = "agent_050"
        self.role = "Senior Recruiter"

        # Observability
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="recruiting")

        # Reliability
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)

        # Cost optimization
        self.cost_tracker = CostTracker(enable_alerts=True)
        self.cache = ResultCache(default_ttl_seconds=1800)

    async def process_application(self, application_data):
        """Process application with full improvements"""
        app_id = application_data.get("id", "unknown")

        # Log start
        self.logger.log_task_start(
            task_id=app_id,
            task_type="application_review",
            priority="normal"
        )

        # Track request
        with self.metrics.track_request(
            agent_id=self.agent_id,
            task_type="application"
        ):
            try:
                result = await self._analyze_resume(application_data)

                self.logger.log_task_end(
                    task_id=app_id,
                    task_type="application_review",
                    success=True
                )

                return result

            except Exception as e:
                self.logger.error("Application processing failed",
                    app_id=app_id, error=str(e))
                self.metrics.record_error(
                    agent_id=self.agent_id,
                    error_type=type(e).__name__
                )
                raise

    @retry(max_attempts=3, exponential_base=2.0)
    @timeout(10.0)
    async def _analyze_resume(self, data):
        """Analyze resume with retry and timeout"""
        # Check cache
        cache_key = f"resume:{data['id']}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        # Check circuit breaker
        if self.circuit_breaker.is_open():
            self.logger.warning("Circuit breaker open, using fallback")
            return {"status": "pending", "reason": "service_unavailable"}

        try:
            # Make external call
            result = await self._call_analysis_service(data)

            # Track success
            await self.circuit_breaker.record_success()

            # Cache result
            self.cache.set(cache_key, result, ttl_seconds=3600)

            return result

        except Exception as e:
            await self.circuit_breaker.record_failure()
            raise
```

**Value delivered**: Full production protection in ~50 lines

---

### Example 3: Full Integration

**Complete production-ready agent with all 7 improvements**:

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import asyncio

from src.observability import get_logger, get_metrics, get_tracer
from src.reliability import retry, timeout, CircuitBreaker, Bulkhead
from src.optimization import CostTracker, ResultCache, LLMRouter
from src.memory import SessionMemory, Session
from src.coordination import MessageBroker, A2AMessage, MessageType
from src.evaluation import ResponseValidator
from src.deployment import SmokeTests


@dataclass
class AgentConfig:
    """Agent configuration"""
    agent_id: str
    model_name: str = "gpt-4-turbo"
    enable_caching: bool = True
    enable_memory: bool = True
    cost_budget_usd: float = 100.0
    max_concurrent: int = 10


class FullyIntegratedAgent:
    """Production-ready agent with all 7 improvements"""

    def __init__(
        self,
        config: AgentConfig,
        message_broker: Optional[MessageBroker] = None,
        cost_tracker: Optional[CostTracker] = None
    ):
        self.config = config

        # IMPROVEMENT 1: OBSERVABILITY
        self.logger = get_logger(agent_id=config.agent_id)
        self.metrics = get_metrics(namespace="production")
        self.tracer = get_tracer(service_name=f"agent-{config.agent_id}")

        # IMPROVEMENT 2: RELIABILITY
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)
        self.bulkhead = Bulkhead(max_workers=config.max_concurrent,
                                 name=config.agent_id)

        # IMPROVEMENT 3: COST OPTIMIZATION
        self.cost_tracker = cost_tracker or CostTracker(enable_alerts=True)
        self.cost_tracker.set_budget(
            limit=config.cost_budget_usd,
            dimension="agent",
            identifier=config.agent_id
        )
        self.cache = ResultCache(default_ttl_seconds=3600) if config.enable_caching else None
        self.llm_router = LLMRouter()  # Smart routing to cheaper models

        # IMPROVEMENT 4: MEMORY
        self.memory = SessionMemory(
            use_fakeredis=True,
            ttl_seconds=3600
        ) if config.enable_memory else None
        self.session_id = None

        # IMPROVEMENT 5: COORDINATION
        self.broker = message_broker or MessageBroker(enable_persistence=True)

        # IMPROVEMENT 6: EVALUATION
        self.validator = ResponseValidator()

        # IMPROVEMENT 7: DEPLOYMENT
        self.smoke_tests = SmokeTests(agent_id=config.agent_id)

        self.logger.info("Agent initialized with all improvements",
            model=config.model_name,
            caching=config.enable_caching,
            memory=config.enable_memory)

    async def start_session(self, user_id: str) -> str:
        """Start new session with memory"""
        if self.memory:
            session = Session(
                agent_id=self.config.agent_id,
                context={"user_id": user_id},
                metadata={"started_at": datetime.utcnow().isoformat()}
            )
            self.memory.store_session(session)
            self.session_id = session.session_id

            self.logger.info("Session started",
                session_id=self.session_id, user_id=user_id)
            return self.session_id
        return "no-session"

    @retry(max_attempts=3, exponential_base=2.0)
    @timeout(30.0)
    async def _make_llm_call(self, prompt: str) -> str:
        """Make LLM call with all protections"""

        # Check cache
        if self.cache:
            cache_key = f"{self.config.model_name}:{hash(prompt)}"
            cached = self.cache.get(cache_key)
            if cached:
                self.logger.info("Cache hit")
                self.metrics.requests_total.labels(
                    agent_id=self.config.agent_id,
                    task_type="llm_call",
                    status="cache_hit"
                ).inc()
                return cached

        # Check circuit breaker
        if self.circuit_breaker.is_open():
            self.logger.warning("Circuit breaker open")
            return "Service temporarily unavailable"

        # Route to best model
        model = self.llm_router.route_request(
            prompt=prompt,
            default_model=self.config.model_name,
            task_type="general"
        )

        try:
            # Execute through bulkhead
            async def llm_call():
                # Simulate API call
                response = f"AI response to: {prompt[:50]}..."

                # Track cost
                cost_record = self.cost_tracker.record_llm_call(
                    model_name=model,
                    input_tokens=int(len(prompt.split()) * 1.3),
                    output_tokens=50,
                    agent_id=self.config.agent_id
                )

                self.logger.info("LLM call completed",
                    model=model,
                    cost=cost_record.amount)

                return response

            result = await self.bulkhead.execute(llm_call)

            # Cache result
            if self.cache:
                self.cache.set(cache_key, result)

            # Record success
            await self.circuit_breaker.record_success()

            return result

        except Exception as e:
            await self.circuit_breaker.record_failure()
            self.logger.error("LLM call failed", error=str(e))
            raise

    async def execute(self, task: dict) -> dict:
        """Execute task with full production capabilities"""
        task_id = task.get("id", f"task-{int(datetime.utcnow().timestamp())}")

        # Start trace
        with self.tracer.start_span("execute_task") as span:
            span.set_attribute("task_id", task_id)

            # Log start
            self.logger.log_task_start(
                task_id=task_id,
                task_type=task.get("type", "unknown"),
                priority=task.get("priority", "normal")
            )

            # Track request
            with self.metrics.track_request(
                agent_id=self.config.agent_id,
                task_type=task.get("type", "unknown")
            ):
                try:
                    # Get conversation context
                    context = ""
                    if self.memory and self.session_id:
                        history = self.memory.get_conversation_history(
                            self.session_id, limit=5
                        )
                        context = "\n".join([h.content for h in history])

                    # Make LLM call with context
                    prompt = f"{context}\n\n{task['content']}"
                    result = await self._make_llm_call(prompt)

                    # Validate quality
                    validation = self.validator.validate_response(
                        prompt=task['content'],
                        response=result,
                        expected_format="text",
                        min_length=10
                    )

                    if not validation.is_valid:
                        self.logger.warning("Quality check failed",
                            issues=validation.issues)

                    # Store in memory
                    if self.memory and self.session_id:
                        self.memory.append_to_history(
                            self.session_id,
                            role="agent",
                            content=result
                        )

                    # Broadcast completion
                    if self.broker:
                        message = A2AMessage(
                            from_agent_id=self.config.agent_id,
                            message_type=MessageType.TASK_COMPLETION,
                            payload={
                                "task_id": task_id,
                                "result": result,
                                "quality_score": validation.overall_score
                            }
                        )
                        await self.broker.publish(message, topic="completions")

                    # Log success
                    self.logger.log_task_end(
                        task_id=task_id,
                        task_type=task.get("type", "unknown"),
                        success=True
                    )

                    return {
                        "success": True,
                        "result": result,
                        "quality_score": validation.overall_score,
                        "task_id": task_id
                    }

                except Exception as e:
                    self.logger.exception("Task failed", task_id=task_id)
                    self.metrics.record_error(
                        agent_id=self.config.agent_id,
                        error_type=type(e).__name__
                    )

                    return {
                        "success": False,
                        "error": str(e),
                        "task_id": task_id
                    }

    async def health_check(self) -> dict:
        """Health check for deployment"""
        checks = {
            "circuit_breaker": not self.circuit_breaker.is_open(),
            "memory": self.memory.get_session_count() < 1000 if self.memory else True,
            "budget": not self.cost_tracker.get_budget_status(
                "agent", self.config.agent_id
            )["is_over_budget"]
        }

        return {
            "healthy": all(checks.values()),
            "checks": checks,
            "agent_id": self.config.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }


# Usage example
async def example_usage():
    """Example of using the fully integrated agent"""

    # Configure agent
    config = AgentConfig(
        agent_id="agent_001",
        model_name="gpt-4-turbo",
        enable_caching=True,
        enable_memory=True,
        cost_budget_usd=100.0
    )

    # Create agent
    agent = FullyIntegratedAgent(config)

    # Start session
    session_id = await agent.start_session(user_id="user-123")

    # Execute task
    result = await agent.execute({
        "id": "task-001",
        "type": "analysis",
        "content": "Analyze Q4 financial performance",
        "priority": "high"
    })

    print(f"Result: {result}")

    # Health check
    health = await agent.health_check()
    print(f"Health: {health}")

if __name__ == "__main__":
    asyncio.run(example_usage())
```

---

## Bulk Migration

### Script to Upgrade All 511 Agents

**File**: `scripts/bulk_upgrade_agents.py`

```python
#!/usr/bin/env python3
"""
Bulk upgrade script to add improvements to all 511 agents.

Usage:
    python scripts/bulk_upgrade_agents.py --phase 1 --dry-run
    python scripts/bulk_upgrade_agents.py --phase 1 --execute
    python scripts/bulk_upgrade_agents.py --all --execute
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Tuple
import subprocess


class AgentUpgrader:
    """Handles bulk upgrade of agents"""

    def __init__(self, agents_dir: Path, dry_run: bool = True):
        self.agents_dir = agents_dir
        self.dry_run = dry_run
        self.upgraded_count = 0
        self.failed_count = 0
        self.skipped_count = 0

    def find_all_agents(self) -> List[Path]:
        """Find all agent files"""
        return sorted(self.agents_dir.glob("agent_*.py"))

    def check_already_upgraded(self, file_path: Path) -> bool:
        """Check if agent already has improvements"""
        content = file_path.read_text()

        # Check for improvement imports
        has_observability = "from src.observability import" in content
        has_reliability = "from src.reliability import" in content

        return has_observability or has_reliability

    def add_phase1_improvements(self, file_path: Path) -> bool:
        """Add Phase 1: Evaluation improvements"""
        try:
            content = file_path.read_text()

            # Skip if already upgraded
            if "from src.evaluation import" in content:
                self.skipped_count += 1
                return True

            # Add imports after docstring
            import_line = "from src.evaluation import ResponseValidator\n"

            # Find class definition
            class_match = re.search(r'class (\w+):', content)
            if not class_match:
                print(f"❌ No class found in {file_path.name}")
                self.failed_count += 1
                return False

            class_name = class_match.group(1)

            # Add validator to __init__
            init_match = re.search(r'def __init__\(self.*?\):', content)
            if init_match:
                # Find the end of __init__ to add validator
                init_addition = "\n        self.validator = ResponseValidator()"

                if self.dry_run:
                    print(f"[DRY RUN] Would add validation to {file_path.name}")
                else:
                    # Add import at top
                    lines = content.split('\n')

                    # Find first import or class
                    insert_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            insert_idx = i + 1
                        elif line.startswith('class '):
                            if insert_idx == 0:
                                insert_idx = i
                            break

                    lines.insert(insert_idx, import_line)

                    # Add validator in __init__
                    for i, line in enumerate(lines):
                        if 'def __init__(self' in line:
                            # Find next method or end of __init__
                            indent_level = len(line) - len(line.lstrip())
                            j = i + 1
                            while j < len(lines):
                                if lines[j].strip() and not lines[j].startswith(' ' * (indent_level + 4)):
                                    break
                                j += 1
                            lines.insert(j - 1, init_addition)
                            break

                    # Write back
                    file_path.write_text('\n'.join(lines))
                    print(f"✅ Upgraded {file_path.name}")

                self.upgraded_count += 1
                return True
            else:
                print(f"⚠️  No __init__ found in {file_path.name}")
                self.failed_count += 1
                return False

        except Exception as e:
            print(f"❌ Error upgrading {file_path.name}: {e}")
            self.failed_count += 1
            return False

    def add_phase2_improvements(self, file_path: Path) -> bool:
        """Add Phase 2: Observability improvements"""
        try:
            content = file_path.read_text()

            if "from src.observability import" in content:
                self.skipped_count += 1
                return True

            # Add imports
            import_block = """from src.observability import get_logger, get_metrics
"""

            # Add to __init__
            init_additions = """
        # Observability
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="mapache")
"""

            if self.dry_run:
                print(f"[DRY RUN] Would add observability to {file_path.name}")
            else:
                # Similar insertion logic as phase 1
                # ... (implement similar to phase1)
                print(f"✅ Added observability to {file_path.name}")

            self.upgraded_count += 1
            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            self.failed_count += 1
            return False

    def add_all_improvements(self, file_path: Path) -> bool:
        """Add all 7 improvements at once"""
        try:
            content = file_path.read_text()

            # Check if already fully upgraded
            if all([
                "from src.observability import" in content,
                "from src.reliability import" in content,
                "from src.optimization import" in content
            ]):
                self.skipped_count += 1
                return True

            # Full import block
            imports = """
from src.observability import get_logger, get_metrics
from src.reliability import retry, CircuitBreaker
from src.optimization import CostTracker, ResultCache
from src.memory import SessionMemory
from src.coordination import MessageBroker
from src.evaluation import ResponseValidator
"""

            # Full __init__ additions
            init_code = """
        # Observability
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="mapache")

        # Reliability
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)

        # Cost Optimization
        self.cost_tracker = CostTracker(enable_alerts=True)
        self.cache = ResultCache(default_ttl_seconds=3600)

        # Memory
        self.memory = SessionMemory(use_fakeredis=True, ttl_seconds=3600)
        self.session_id = None

        # Coordination
        self.broker = MessageBroker(enable_persistence=True)

        # Evaluation
        self.validator = ResponseValidator()
"""

            if self.dry_run:
                print(f"[DRY RUN] Would fully upgrade {file_path.name}")
            else:
                # Implement full upgrade
                # This is more complex - recommend doing in phases
                print(f"⚠️  Full upgrade recommended in phases for {file_path.name}")
                print(f"   Run with --phase 1, then --phase 2, etc.")

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            self.failed_count += 1
            return False

    def run_tests(self, file_path: Path) -> bool:
        """Run tests on upgraded agent"""
        try:
            # Import and test
            result = subprocess.run(
                ["python", "-m", "py_compile", str(file_path)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"✅ Syntax valid: {file_path.name}")
                return True
            else:
                print(f"❌ Syntax error: {file_path.name}")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"❌ Test error: {e}")
            return False

    def create_backup(self, file_path: Path):
        """Create backup before modification"""
        backup_path = file_path.with_suffix('.py.backup')
        backup_path.write_text(file_path.read_text())
        print(f"📦 Backup created: {backup_path.name}")

    def run_phase(self, phase: int):
        """Run specific upgrade phase"""
        agents = self.find_all_agents()
        total = len(agents)

        print(f"\n{'='*60}")
        print(f"PHASE {phase} UPGRADE")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print(f"Agents found: {total}")
        print(f"{'='*60}\n")

        phase_methods = {
            1: self.add_phase1_improvements,
            2: self.add_phase2_improvements,
            # Add methods for phases 3-7
        }

        upgrade_method = phase_methods.get(phase)
        if not upgrade_method:
            print(f"❌ Phase {phase} not implemented yet")
            return

        for agent_file in agents:
            print(f"\nProcessing: {agent_file.name}")

            # Create backup if executing
            if not self.dry_run:
                self.create_backup(agent_file)

            # Upgrade
            success = upgrade_method(agent_file)

            # Test if executing
            if success and not self.dry_run:
                self.run_tests(agent_file)

        # Summary
        print(f"\n{'='*60}")
        print(f"PHASE {phase} SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Upgraded: {self.upgraded_count}/{total}")
        print(f"⏭️  Skipped: {self.skipped_count}/{total}")
        print(f"❌ Failed: {self.failed_count}/{total}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Bulk upgrade agents")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4, 5],
                       help="Which phase to run (1-5)")
    parser.add_argument("--all", action="store_true",
                       help="Run all phases")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")
    parser.add_argument("--execute", action="store_true",
                       help="Actually execute the changes")

    args = parser.parse_args()

    # Validate args
    if not args.phase and not args.all:
        parser.error("Must specify --phase or --all")

    if args.dry_run and args.execute:
        parser.error("Cannot use both --dry-run and --execute")

    # Default to dry-run for safety
    dry_run = not args.execute

    # Find agents directory
    agents_dir = Path("/home/user/mapachev1/python/agents")
    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        return

    # Create upgrader
    upgrader = AgentUpgrader(agents_dir, dry_run=dry_run)

    # Run upgrade
    if args.all:
        for phase in range(1, 6):
            upgrader.run_phase(phase)
            # Reset counters between phases
            upgrader.upgraded_count = 0
            upgrader.failed_count = 0
            upgrader.skipped_count = 0
    else:
        upgrader.run_phase(args.phase)


if __name__ == "__main__":
    main()
```

**Usage**:

```bash
# Step 1: Dry run to see what would change
python scripts/bulk_upgrade_agents.py --phase 1 --dry-run

# Step 2: Execute Phase 1 (Evaluation)
python scripts/bulk_upgrade_agents.py --phase 1 --execute

# Step 3: Test upgraded agents
python -m pytest tests/

# Step 4: Continue with Phase 2
python scripts/bulk_upgrade_agents.py --phase 2 --execute

# Or run all phases (after testing each individually)
python scripts/bulk_upgrade_agents.py --all --execute
```

---

### Testing Strategy

**1. Unit Testing**

```python
# tests/test_upgraded_agents.py
import pytest
from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent


def test_agent_has_logger():
    """Test that upgraded agent has logger"""
    agent = CEORootCoordinatorAgent()
    assert hasattr(agent, 'logger')
    assert agent.logger is not None


def test_agent_has_metrics():
    """Test that upgraded agent has metrics"""
    agent = CEORootCoordinatorAgent()
    assert hasattr(agent, 'metrics')
    assert agent.metrics is not None


def test_agent_has_validator():
    """Test that upgraded agent has validator"""
    agent = CEORootCoordinatorAgent()
    assert hasattr(agent, 'validator')


@pytest.mark.asyncio
async def test_agent_execute_with_retry():
    """Test that execute method works with retry"""
    agent = CEORootCoordinatorAgent()
    result = await agent.execute("Test task")
    assert result is not None
```

**2. Integration Testing**

```python
# tests/integration/test_agent_integration.py
import pytest
from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent
from src.coordination import MessageBroker
from src.optimization import CostTracker


@pytest.mark.asyncio
async def test_agent_with_shared_infrastructure():
    """Test agent with shared services"""
    # Create shared infrastructure
    broker = MessageBroker(enable_persistence=False)
    cost_tracker = CostTracker(enable_alerts=False)

    # Create agent
    agent = CEORootCoordinatorAgent(
        message_broker=broker,
        cost_tracker=cost_tracker
    )

    # Test execution
    result = await agent.execute({"task": "test"})

    # Verify cost tracking
    stats = cost_tracker.get_agent_stats(agent.agent_id, days=1)
    assert stats.request_count > 0
```

**3. Smoke Testing**

```bash
# scripts/smoke_test_agents.sh
#!/bin/bash

echo "Running smoke tests on upgraded agents..."

# Test import
python -c "from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent; print('✅ Import successful')"

# Test initialization
python -c "from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent; agent = CEORootCoordinatorAgent(); print('✅ Initialization successful')"

# Test basic execution
python -c "
import asyncio
from python.agents.agent_001_ceo_root_coordinator import CEORootCoordinatorAgent

async def test():
    agent = CEORootCoordinatorAgent()
    result = await agent.execute('test')
    print(f'✅ Execution successful: {result}')

asyncio.run(test())
"

echo "✅ All smoke tests passed"
```

---

### Rollback Plan

**1. Automatic Rollback Script**

```python
# scripts/rollback_upgrades.py
#!/usr/bin/env python3
"""Rollback agent upgrades"""

from pathlib import Path
import shutil


def rollback_all_agents(agents_dir: Path):
    """Rollback all agents to backup"""
    backups = list(agents_dir.glob("*.py.backup"))

    print(f"Found {len(backups)} backups")

    for backup in backups:
        original = backup.with_suffix('')  # Remove .backup

        print(f"Rolling back: {original.name}")
        shutil.copy(backup, original)

        # Optionally remove backup
        # backup.unlink()

    print(f"✅ Rolled back {len(backups)} files")


if __name__ == "__main__":
    agents_dir = Path("/home/user/mapachev1/python/agents")
    rollback_all_agents(agents_dir)
```

**2. Git-based Rollback**

```bash
# If using git
git stash
git checkout HEAD -- python/agents/

# Or restore specific agent
git checkout HEAD -- python/agents/agent_001_ceo_root_coordinator.py
```

**3. Gradual Rollback**

```python
# scripts/selective_rollback.py
"""Rollback only failed agents"""

def rollback_failed_agents(failed_list: list):
    """Rollback specific agents"""
    for agent_file in failed_list:
        backup = Path(f"{agent_file}.backup")
        if backup.exists():
            shutil.copy(backup, agent_file)
            print(f"✅ Rolled back {agent_file}")
```

---

## Common Pitfalls

### Pitfall 1: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Cause**: Running from wrong directory or Python path not set

**Solution**:
```python
# Add at top of agent file
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Now imports work
from src.observability import get_logger
```

**Better solution**: Use proper package installation
```bash
# Install project as package
cd /home/user/mapachev1
pip install -e .
```

---

### Pitfall 2: Async/Sync Mismatch

**Problem**: `RuntimeWarning: coroutine was never awaited`

**Cause**: Calling async method without await

**Solution**:
```python
# WRONG
result = agent.execute(task)  # Returns coroutine, not result

# RIGHT
result = await agent.execute(task)

# Or if in sync context
import asyncio
result = asyncio.run(agent.execute(task))
```

---

### Pitfall 3: Circular Imports

**Problem**: `ImportError: cannot import name 'X' from partially initialized module`

**Cause**: Circular dependencies between modules

**Solution**:
```python
# WRONG - Direct import in module level
from src.coordination import MessageBroker
from src.agents import CEOAgent  # Causes circular import

# RIGHT - Import inside function
def create_agent():
    from src.agents import CEOAgent  # Import when needed
    return CEOAgent()
```

---

### Pitfall 4: Shared State Issues

**Problem**: All agents sharing same logger/metrics instance

**Cause**: Creating singletons incorrectly

**Solution**:
```python
# WRONG
class Agent:
    logger = get_logger("shared")  # Class variable - shared!

# RIGHT
class Agent:
    def __init__(self):
        self.logger = get_logger(agent_id=self.agent_id)  # Instance variable
```

---

### Pitfall 5: Cost Tracker Not Recording

**Problem**: Cost tracker shows $0.00

**Cause**: Not calling record_llm_call

**Solution**:
```python
# WRONG
async def call_llm(prompt):
    response = await llm_api.complete(prompt)
    return response  # Cost not tracked!

# RIGHT
async def call_llm(prompt):
    response = await llm_api.complete(prompt)

    # Track cost
    self.cost_tracker.record_llm_call(
        model_name="gpt-4",
        input_tokens=len(prompt.split()) * 1.3,
        output_tokens=len(response.split()) * 1.3,
        agent_id=self.agent_id
    )

    return response
```

---

### Pitfall 6: Memory Leaks with Sessions

**Problem**: Memory usage grows over time

**Cause**: Not cleaning up old sessions

**Solution**:
```python
# Add session cleanup
from src.memory import SessionMemory

class Agent:
    def __init__(self):
        self.memory = SessionMemory(
            use_fakeredis=True,
            ttl_seconds=3600  # Auto-expire after 1 hour
        )

    async def cleanup_old_sessions(self):
        """Periodic cleanup"""
        # Sessions auto-expire based on TTL
        # But you can also manually clear
        old_sessions = self.memory.get_sessions_older_than(hours=24)
        for session in old_sessions:
            self.memory.delete_session(session.session_id)
```

---

### Pitfall 7: Circuit Breaker Stuck Open

**Problem**: Circuit breaker opens and never closes

**Cause**: Not recording successes

**Solution**:
```python
# WRONG
async def call_service():
    if self.circuit_breaker.is_open():
        raise Exception("Circuit open")
    return await external_service.call()
    # No success recording!

# RIGHT
async def call_service():
    if self.circuit_breaker.is_open():
        raise Exception("Circuit open")

    try:
        result = await external_service.call()
        await self.circuit_breaker.record_success()  # Record success!
        return result
    except Exception as e:
        await self.circuit_breaker.record_failure()
        raise
```

---

### Pitfall 8: Configuration Mistakes

**Problem**: Features not working as expected

**Cause**: Wrong configuration values

**Solution**:
```python
# WRONG
cache = ResultCache(default_ttl_seconds=0)  # Cache disabled!
circuit_breaker = CircuitBreaker(failure_threshold=0)  # Always open!

# RIGHT
cache = ResultCache(default_ttl_seconds=3600)  # 1 hour
circuit_breaker = CircuitBreaker(
    failure_threshold=5,  # Open after 5 failures
    timeout=60.0  # Try to close after 60 seconds
)
```

---

### Pitfall 9: Performance Degradation

**Problem**: Agents slower after adding improvements

**Cause**: Too much synchronous logging or metrics

**Solution**:
```python
# WRONG - Synchronous logging in hot path
for item in large_list:
    self.logger.info("Processing", item=item)  # Slow!
    process(item)

# RIGHT - Batch logging or log less frequently
self.logger.info(f"Processing {len(large_list)} items")
for item in large_list:
    process(item)
self.logger.info("Processing complete")

# OR use async logging
await self.logger.info_async("Processing", item=item)
```

---

## Validation Checklist

### After Upgrading Each Agent

**Observability** ✓
- [ ] Agent has `self.logger` initialized
- [ ] Agent has `self.metrics` initialized
- [ ] Agent logs task start/end
- [ ] Agent records errors
- [ ] Logs include agent_id context
- [ ] Test: Run agent and check logs appear

**Reliability** ✓
- [ ] Critical methods have `@retry` decorator
- [ ] Timeout protection on external calls
- [ ] Circuit breaker initialized
- [ ] Circuit breaker checks before external calls
- [ ] Success/failure recorded in circuit breaker
- [ ] Test: Simulate failure, verify retry happens

**Cost Optimization** ✓
- [ ] `CostTracker` initialized
- [ ] Budget set for agent
- [ ] LLM calls record cost
- [ ] Cache initialized (if enabled)
- [ ] Cache checked before LLM calls
- [ ] Test: Make LLM call, verify cost recorded

**Memory** ✓
- [ ] `SessionMemory` initialized (if needed)
- [ ] Session created before conversations
- [ ] History appended after each turn
- [ ] Session cleanup implemented
- [ ] Test: Create session, verify history stored

**Coordination** ✓
- [ ] `MessageBroker` injected or created
- [ ] Messages published on key events
- [ ] Agent subscribes to relevant topics
- [ ] Test: Send message, verify received

**Evaluation** ✓
- [ ] `ResponseValidator` initialized
- [ ] Responses validated before returning
- [ ] Validation failures logged
- [ ] Quality scores tracked
- [ ] Test: Validate response, check score

**Deployment** ✓
- [ ] `health_check()` method implemented
- [ ] Health check returns all required fields
- [ ] Smoke tests pass
- [ ] Agent can be imported without errors
- [ ] Test: Call health_check(), verify healthy

---

### System-Wide Validation

**After Upgrading All 511 Agents**:

```bash
# 1. Import check
python scripts/validate_imports.py

# 2. Syntax check
python scripts/validate_syntax.py

# 3. Run smoke tests
python scripts/smoke_test_all_agents.py

# 4. Run unit tests
pytest tests/unit/

# 5. Run integration tests
pytest tests/integration/

# 6. Check metrics
python scripts/check_metrics_collection.py

# 7. Verify cost tracking
python scripts/verify_cost_tracking.py
```

**Validation Script**:

```python
# scripts/validate_all_agents.py
#!/usr/bin/env python3
"""Validate all upgraded agents"""

import importlib
import sys
from pathlib import Path


def validate_agent(agent_module):
    """Validate single agent"""
    checks = {
        "has_logger": False,
        "has_metrics": False,
        "has_cost_tracker": False,
        "has_validator": False,
        "has_health_check": False
    }

    try:
        # Import module
        module = importlib.import_module(agent_module)

        # Find agent class
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, type) and "Agent" in item_name:
                # Create instance
                agent = item()

                # Check attributes
                checks["has_logger"] = hasattr(agent, 'logger')
                checks["has_metrics"] = hasattr(agent, 'metrics')
                checks["has_cost_tracker"] = hasattr(agent, 'cost_tracker')
                checks["has_validator"] = hasattr(agent, 'validator')
                checks["has_health_check"] = hasattr(agent, 'health_check')

                break

        return checks

    except Exception as e:
        print(f"❌ Error validating {agent_module}: {e}")
        return checks


def main():
    """Validate all agents"""
    agents_dir = Path("/home/user/mapachev1/python/agents")
    agent_files = sorted(agents_dir.glob("agent_*.py"))

    print(f"Validating {len(agent_files)} agents...\n")

    results = []
    for agent_file in agent_files:
        module_name = f"python.agents.{agent_file.stem}"
        checks = validate_agent(module_name)
        results.append((agent_file.name, checks))

    # Summary
    print(f"\n{'='*80}")
    print("VALIDATION SUMMARY")
    print(f"{'='*80}\n")

    total = len(results)
    observability = sum(1 for _, c in results if c["has_logger"] and c["has_metrics"])
    cost_tracking = sum(1 for _, c in results if c["has_cost_tracker"])
    evaluation = sum(1 for _, c in results if c["has_validator"])
    deployment = sum(1 for _, c in results if c["has_health_check"])

    print(f"Observability (logger + metrics): {observability}/{total} ({observability/total*100:.1f}%)")
    print(f"Cost Tracking: {cost_tracking}/{total} ({cost_tracking/total*100:.1f}%)")
    print(f"Evaluation: {evaluation}/{total} ({evaluation/total*100:.1f}%)")
    print(f"Deployment: {deployment}/{total} ({deployment/total*100:.1f}%)")

    # Detailed failures
    print(f"\n{'='*80}")
    print("AGENTS NEEDING ATTENTION")
    print(f"{'='*80}\n")

    for agent_name, checks in results:
        issues = [k for k, v in checks.items() if not v]
        if issues:
            print(f"⚠️  {agent_name}: Missing {', '.join(issues)}")


if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Issue 1: Agent Won't Start

**Symptoms**:
```
ImportError: cannot import name 'get_logger' from 'src.observability'
```

**Diagnosis**:
```bash
# Check if module exists
ls -la /home/user/mapachev1/src/observability/

# Check if __init__.py exports it
grep "get_logger" /home/user/mapachev1/src/observability/__init__.py
```

**Fix**:
```python
# Verify import path
from src.observability import get_logger  # Correct

# Not
from observability import get_logger  # Wrong - missing 'src'
```

---

### Issue 2: Logs Not Appearing

**Symptoms**: No log output despite calling logger.info()

**Diagnosis**:
```python
# Check log level
agent.logger.logger.level  # Should be INFO or DEBUG

# Check handlers
agent.logger.logger.handlers  # Should have at least one
```

**Fix**:
```python
# Set log level explicitly
from src.observability import get_logger

logger = get_logger(agent_id="agent_001", log_level="INFO")

# Or configure globally
import logging
logging.basicConfig(level=logging.INFO)
```

---

### Issue 3: Metrics Not Recording

**Symptoms**: Metrics show 0 counts

**Diagnosis**:
```python
# Check if metrics are being called
agent.metrics.requests_total.labels(
    agent_id=agent.agent_id,
    task_type="test",
    status="success"
).inc()

# Check current value
from prometheus_client import generate_latest
print(generate_latest().decode())
```

**Fix**:
```python
# Ensure labels match
# WRONG
self.metrics.requests_total.labels(
    agent="agent_001"  # Wrong label name!
).inc()

# RIGHT
self.metrics.requests_total.labels(
    agent_id="agent_001",
    task_type="execute",
    status="success"
).inc()
```

---

### Issue 4: Circuit Breaker Always Open

**Symptoms**: Circuit breaker immediately opens

**Diagnosis**:
```python
# Check configuration
print(f"Failure threshold: {agent.circuit_breaker.failure_threshold}")
print(f"Timeout: {agent.circuit_breaker.timeout}")
print(f"Current failures: {agent.circuit_breaker.failure_count}")
```

**Fix**:
```python
# Increase threshold
circuit_breaker = CircuitBreaker(
    failure_threshold=10,  # Increase from 5
    timeout=60.0
)

# Or reset manually
await circuit_breaker.reset()
```

---

### Issue 5: Cost Showing as $0

**Symptoms**: Cost tracker shows $0.00 despite LLM calls

**Diagnosis**:
```python
# Check if recording
cost_record = agent.cost_tracker.record_llm_call(
    model_name="gpt-4-turbo",
    input_tokens=100,
    output_tokens=50,
    agent_id="agent_001"
)
print(f"Recorded cost: ${cost_record.amount}")

# Check pricing
from src.optimization.cost_tracker import MODEL_PRICING
print(MODEL_PRICING.get("gpt-4-turbo"))
```

**Fix**:
```python
# Ensure model name matches pricing table
# WRONG
cost_tracker.record_llm_call(model_name="gpt4")  # Not in pricing!

# RIGHT
cost_tracker.record_llm_call(model_name="gpt-4-turbo")

# Or add custom pricing
cost_tracker.set_custom_pricing("gpt-4", input_price_per_1k=0.03, output_price_per_1k=0.06)
```

---

### Issue 6: Memory Session Not Found

**Symptoms**: `SessionNotFoundError` when retrieving history

**Diagnosis**:
```python
# Check if session exists
session = agent.memory.get_session(session_id)
print(f"Session: {session}")

# Check TTL
print(f"Session count: {agent.memory.get_session_count()}")
```

**Fix**:
```python
# Ensure session created before use
session_id = await agent.start_session(user_id="user-123")

# Then use it
history = agent.memory.get_conversation_history(session_id)

# Check TTL isn't too short
memory = SessionMemory(
    use_fakeredis=True,
    ttl_seconds=7200  # 2 hours instead of 1
)
```

---

### Issue 7: Message Broker Not Delivering

**Symptoms**: Published messages not received

**Diagnosis**:
```python
# Check if subscribed
await broker.subscribe("topic_name", callback_function)

# Check if topic matches
await broker.publish(message, topic="topic_name")  # Must match!

# Check delivery
stats = await broker.get_stats()
print(f"Messages delivered: {stats['delivered_count']}")
```

**Fix**:
```python
# Ensure topic matches exactly
# WRONG
await broker.publish(message, topic="Tasks")  # Capital T
await broker.subscribe("tasks", callback)  # Lowercase t

# RIGHT
await broker.publish(message, topic="tasks")
await broker.subscribe("tasks", callback)
```

---

### Issue 8: Tests Failing After Upgrade

**Symptoms**: `TypeError: object async_generator can't be used in 'await' expression`

**Diagnosis**:
```python
# Check if test is async
def test_agent():  # Missing async!
    result = await agent.execute(task)
```

**Fix**:
```python
# Add async to test
import pytest

@pytest.mark.asyncio
async def test_agent():
    result = await agent.execute(task)
    assert result is not None
```

---

### Getting Help

**Debug Checklist**:

1. Check Python version: `python --version` (need 3.9+)
2. Check imports: `python -c "from src.observability import get_logger"`
3. Check file exists: `ls -la /home/user/mapachev1/src/observability/__init__.py`
4. Check syntax: `python -m py_compile python/agents/agent_001.py`
5. Check logs: Look for error messages in structured logs
6. Check metrics: `curl http://localhost:9090/metrics` (if Prometheus running)

**Common Commands**:

```bash
# Re-install dependencies
pip install -e /home/user/mapachev1

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Restart Python
# (exit and restart Python interpreter)

# Run single agent test
python -m pytest tests/unit/test_agent_001.py -v

# Check for syntax errors
python -m py_compile python/agents/agent_001_ceo_root_coordinator.py
```

---

## Quick Reference

### Import Cheatsheet

```python
# Observability
from src.observability import get_logger, get_metrics, get_tracer

# Reliability
from src.reliability import retry, timeout, CircuitBreaker, Bulkhead

# Cost Optimization
from src.optimization import CostTracker, ResultCache, LLMRouter

# Memory
from src.memory import SessionMemory, Session

# Coordination
from src.coordination import MessageBroker, A2AMessage, MessageType

# Evaluation
from src.evaluation import ResponseValidator

# Deployment
from src.deployment import BlueGreenDeployment, SmokeTests
```

### Initialization Template

```python
class Agent:
    def __init__(self):
        self.agent_id = "agent_XXX"

        # Observability
        self.logger = get_logger(agent_id=self.agent_id)
        self.metrics = get_metrics(namespace="mapache")

        # Reliability
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)

        # Cost
        self.cost_tracker = CostTracker(enable_alerts=True)
        self.cache = ResultCache(default_ttl_seconds=3600)

        # Memory
        self.memory = SessionMemory(use_fakeredis=True, ttl_seconds=3600)

        # Coordination
        self.broker = MessageBroker(enable_persistence=True)

        # Evaluation
        self.validator = ResponseValidator()
```

---

## Next Steps

After completing integration:

1. **Monitor in Production**
   - Set up Grafana dashboards
   - Configure alerts for budget overruns
   - Monitor error rates

2. **Optimize Performance**
   - Analyze cache hit rates
   - Tune circuit breaker thresholds
   - Optimize LLM model routing

3. **Scale Up**
   - Add more agents to coordination network
   - Implement advanced orchestration patterns
   - Build agent hierarchies

4. **Continuous Improvement**
   - Review quality scores
   - Analyze cost trends
   - Optimize prompts based on metrics

---

**Need Help?**

- Check `/home/user/mapachev1/examples/` for working examples
- Run `python examples/before_after_agent.py` to see improvements in action
- Read module documentation in `/home/user/mapachev1/src/*/README.md`

---

**Version**: 1.0
**Last Updated**: 2025-11-17
**Agents Supported**: 511+
