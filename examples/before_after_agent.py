#!/usr/bin/env python3
"""
Before/After Agent Comparison

This example demonstrates the dramatic difference between a basic agent and a
production-ready agent with all 7 improvements integrated:

1. Observability - Structured logging, metrics, and tracing
2. Reliability - Retry logic, circuit breakers, and timeouts
3. Cost Optimization - Cost tracking, model routing, and caching
4. Memory Management - Session memory and context tracking
5. Coordination - A2A protocol and message broker
6. Evaluation - Quality gates and validation
7. Deployment - Safe deployment patterns

Run this example to see side-by-side comparison with metrics.
"""

import asyncio
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# BEFORE: Basic imports - just need requests or HTTP client
# AFTER: Rich imports from our improvement framework
from src.observability.structured_logging import AgentLogger
from src.observability.metrics import AgentMetrics
from src.reliability.retry import retry
from src.reliability.circuit_breaker import CircuitBreaker
from src.optimization.cost_tracker import CostTracker, CostCategory
from src.optimization.caching import ResultCache
from src.memory.session_memory import SessionMemory, Session, SessionEntry
from src.coordination.a2a_protocol import A2AMessage, MessageType
from src.coordination.message_broker import MessageBroker


# ==============================================================================
# BEFORE: Basic Agent (No Improvements)
# ==============================================================================

class BasicAgent:
    """
    BEFORE: A basic agent with just LLM calls.

    Problems:
    - No logging or observability
    - No error handling or retry logic
    - No cost tracking
    - No memory management
    - No performance metrics
    - No coordination capabilities
    - Fails silently on errors
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.call_count = 0

    def process_task(self, task: str) -> str:
        """Process a task with just a basic LLM call."""
        self.call_count += 1

        # Simulate LLM call
        time.sleep(0.1)  # Simulated API latency

        # No error handling - if this fails, everything fails
        result = f"Processed: {task}"

        # No logging, no metrics, no cost tracking
        return result

    def get_stats(self) -> Dict[str, Any]:
        """Get basic stats - just a counter."""
        return {"call_count": self.call_count}


# ==============================================================================
# AFTER: Production-Ready Agent (All 7 Improvements)
# ==============================================================================

@dataclass
class AgentConfig:
    """Configuration for production agent."""
    agent_id: str
    model_name: str = "gpt-4-turbo"
    enable_caching: bool = True
    enable_memory: bool = True
    max_retries: int = 3
    timeout_seconds: float = 30.0
    cost_budget_usd: float = 10.0


class ProductionAgent:
    """
    AFTER: Production-ready agent with all 7 improvements integrated.

    Improvements:
    1. OBSERVABILITY: Structured logging, metrics collection, tracing
    2. RELIABILITY: Retry logic, circuit breakers, timeouts, error handling
    3. COST OPTIMIZATION: Cost tracking, caching, budget management
    4. MEMORY: Session memory, conversation history, context management
    5. COORDINATION: A2A messaging, pub/sub communication
    6. EVALUATION: Quality validation, performance tracking
    7. DEPLOYMENT: Health checks, graceful degradation
    """

    def __init__(
        self,
        config: AgentConfig,
        logger: Optional[AgentLogger] = None,
        metrics: Optional[AgentMetrics] = None,
        cost_tracker: Optional[CostTracker] = None,
        message_broker: Optional[MessageBroker] = None,
    ):
        self.config = config

        # IMPROVEMENT 1: OBSERVABILITY - Structured logging and metrics
        self.logger = logger or AgentLogger(
            agent_id=config.agent_id,
            environment="production",
            log_level="INFO"
        )
        self.metrics = metrics or AgentMetrics(
            namespace="agent",
            subsystem="production"
        )

        # IMPROVEMENT 2: RELIABILITY - Circuit breaker for external calls
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout=60.0
        )

        # IMPROVEMENT 3: COST OPTIMIZATION - Track and manage costs
        self.cost_tracker = cost_tracker or CostTracker(enable_alerts=True)
        self.cost_tracker.set_budget(
            limit=config.cost_budget_usd,
            dimension="agent",
            identifier=config.agent_id
        )

        # IMPROVEMENT 3: COST OPTIMIZATION - Cache responses
        self.cache = ResultCache(default_ttl_seconds=3600) if config.enable_caching else None

        # IMPROVEMENT 4: MEMORY - Session memory for context
        self.memory = SessionMemory(
            use_fakeredis=True,
            ttl_seconds=3600
        ) if config.enable_memory else None

        # IMPROVEMENT 5: COORDINATION - Message broker for A2A communication
        self.broker = message_broker

        # Internal state
        self.session_id: Optional[str] = None
        self.total_cost = 0.0

        self.logger.info(
            "Production agent initialized",
            model=config.model_name,
            caching=config.enable_caching,
            memory=config.enable_memory
        )

    async def start_session(self) -> str:
        """Start a new session with memory tracking."""
        if self.memory:
            session = Session(
                agent_id=self.config.agent_id,
                context={"model": self.config.model_name},
                metadata={"started_at": datetime.utcnow().isoformat()}
            )
            self.memory.store_session(session)
            self.session_id = session.session_id

            self.logger.info(
                "Session started",
                session_id=self.session_id
            )

            return self.session_id
        return "no-session"

    @retry(max_attempts=3, exponential_base=2.0)
    async def _make_llm_call(
        self,
        prompt: str,
        session_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Make an LLM call with retry logic.

        IMPROVEMENT 2: RELIABILITY - Automatic retry with exponential backoff
        """
        # IMPROVEMENT 3: Check cache first
        if self.cache:
            cache_key = f"{self.config.model_name}:{prompt}"
            cached_response = self.cache.get(cache_key)
            if cached_response:
                self.logger.info("Cache hit", cache_key=cache_key[:50])
                self.metrics.requests_total.labels(
                    agent_id=self.config.agent_id,
                    task_type="llm_call",
                    status="cache_hit"
                ).inc()
                return cached_response

        # IMPROVEMENT 2: Circuit breaker protects against cascading failures
        if self.circuit_breaker.is_open():
            self.logger.warning("Circuit breaker is open, using fallback")
            return "Circuit breaker open - service temporarily unavailable"

        # Simulate LLM API call with realistic behavior
        start_time = time.time()

        try:
            # Simulate API call
            await asyncio.sleep(0.1)  # Simulated latency

            # Simulate realistic token usage
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            output_tokens = 50  # Simulated response length

            response = f"AI Response to: {prompt[:50]}..."

            # IMPROVEMENT 3: Track costs automatically
            cost_record = self.cost_tracker.record_llm_call(
                model_name=self.config.model_name,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                agent_id=self.config.agent_id,
                metadata={"prompt_preview": prompt[:100]}
            )

            self.total_cost += cost_record.amount

            # IMPROVEMENT 1: Record metrics
            duration = time.time() - start_time
            self.metrics.record_llm_tokens(
                agent_id=self.config.agent_id,
                model=self.config.model_name,
                prompt_tokens=int(input_tokens),
                completion_tokens=int(output_tokens)
            )
            self.metrics.record_cost(
                agent_id=self.config.agent_id,
                cost_usd=cost_record.amount,
                cost_type="llm"
            )

            # IMPROVEMENT 3: Cache the response
            if self.cache:
                cache_key = f"{self.config.model_name}:{prompt}"
                self.cache.set(cache_key, response)

            # IMPROVEMENT 2: Record success in circuit breaker
            await self.circuit_breaker.record_success()

            self.logger.info(
                "LLM call completed",
                duration_ms=duration * 1000,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                cost_usd=cost_record.amount
            )

            return response

        except Exception as e:
            # IMPROVEMENT 2: Record failure in circuit breaker
            await self.circuit_breaker.record_failure()

            # IMPROVEMENT 1: Structured error logging
            self.logger.error(
                "LLM call failed",
                error=str(e),
                error_type=type(e).__name__
            )
            self.metrics.record_error(
                agent_id=self.config.agent_id,
                error_type=type(e).__name__
            )
            raise

    async def process_task(
        self,
        task: str,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Process a task with full production capabilities.

        Returns detailed results including metrics, costs, and status.
        """
        task_id = f"task-{int(time.time() * 1000)}"

        # IMPROVEMENT 1: Log task start
        self.logger.log_task_start(
            task_id=task_id,
            task_type="process",
            priority=priority,
            task_preview=task[:100]
        )

        # IMPROVEMENT 1: Track request metrics
        with self.metrics.track_request(
            agent_id=self.config.agent_id,
            task_type="process"
        ):
            start_time = time.time()
            success = False
            result_data = None
            error_msg = None

            try:
                # IMPROVEMENT 4: Add to session memory
                if self.memory and self.session_id:
                    self.memory.append_to_history(
                        session_id=self.session_id,
                        role="user",
                        content=task,
                        metadata={"priority": priority, "task_id": task_id}
                    )

                # IMPROVEMENT 2: Apply timeout to prevent hanging
                async def process_with_timeout():
                    return await self._make_llm_call(task)

                result = await asyncio.wait_for(
                    process_with_timeout(),
                    timeout=self.config.timeout_seconds
                )

                result_data = result
                success = True

                # IMPROVEMENT 4: Store result in memory
                if self.memory and self.session_id:
                    self.memory.append_to_history(
                        session_id=self.session_id,
                        role="agent",
                        content=result,
                        metadata={"task_id": task_id}
                    )

                # IMPROVEMENT 5: Broadcast task completion via A2A
                if self.broker:
                    message = A2AMessage(
                        from_agent_id=self.config.agent_id,
                        message_type=MessageType.TASK_COMPLETION,
                        payload={
                            "task_id": task_id,
                            "result": result,
                            "success": True
                        }
                    )
                    await self.broker.publish(message, topic="task_completions")

            except asyncio.TimeoutError:
                error_msg = f"Task timed out after {self.config.timeout_seconds}s"
                self.logger.error("Task timeout", task_id=task_id)

            except Exception as e:
                error_msg = f"Task failed: {str(e)}"
                self.logger.exception("Task failed", task_id=task_id, error=str(e))

            duration = time.time() - start_time

            # IMPROVEMENT 1: Log task completion
            self.logger.log_task_end(
                task_id=task_id,
                task_type="process",
                success=success,
                duration_ms=duration * 1000
            )

            # IMPROVEMENT 6: Quality validation
            quality_score = self._evaluate_quality(result_data) if success else 0.0

            # Build comprehensive result
            return {
                "task_id": task_id,
                "success": success,
                "result": result_data,
                "error": error_msg,
                "metrics": {
                    "duration_ms": duration * 1000,
                    "cost_usd": self.cost_tracker.get_agent_stats(
                        self.config.agent_id, days=1
                    ).total_cost,
                    "quality_score": quality_score,
                    "cached": False  # Could track this from cache hits
                },
                "session_id": self.session_id
            }

    def _evaluate_quality(self, result: Optional[str]) -> float:
        """
        IMPROVEMENT 6: EVALUATION - Assess result quality.

        In production, this would use more sophisticated validation.
        """
        if not result:
            return 0.0

        # Simple heuristic scoring
        score = 1.0

        # Penalize very short responses
        if len(result) < 10:
            score *= 0.5

        # Reward longer, more detailed responses
        if len(result) > 100:
            score *= 1.2

        return min(score, 1.0)

    async def get_comprehensive_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics across all dimensions.

        IMPROVEMENT 1 & 3: Rich observability and cost tracking.
        """
        # Cost stats
        cost_stats = self.cost_tracker.get_agent_stats(
            self.config.agent_id,
            days=1
        )

        # Budget status
        budget_status = self.cost_tracker.get_budget_status(
            dimension="agent",
            identifier=self.config.agent_id
        )

        # Session stats
        session_count = self.memory.get_session_count() if self.memory else 0

        # Circuit breaker state
        cb_state = self.circuit_breaker.state.value

        # Cache stats
        cache_stats = self.cache.get_stats() if self.cache else {}

        return {
            "agent_id": self.config.agent_id,
            "costs": {
                "total_cost_usd": cost_stats.total_cost,
                "total_tokens": cost_stats.total_tokens,
                "requests": cost_stats.request_count,
                "avg_cost_per_request": cost_stats.average_cost_per_request,
                "budget_remaining": budget_status["remaining"],
                "budget_used_pct": budget_status["percentage_used"]
            },
            "reliability": {
                "circuit_breaker_state": cb_state,
                "max_retries": self.config.max_retries,
                "timeout_seconds": self.config.timeout_seconds
            },
            "memory": {
                "active_sessions": session_count,
                "current_session_id": self.session_id
            },
            "performance": {
                "cache_enabled": self.config.enable_caching,
                "cache_stats": cache_stats
            },
            "model": self.config.model_name
        }

    async def health_check(self) -> Dict[str, Any]:
        """
        IMPROVEMENT 7: DEPLOYMENT - Health check for monitoring.
        """
        is_healthy = True
        issues = []

        # Check circuit breaker
        if self.circuit_breaker.is_open():
            is_healthy = False
            issues.append("Circuit breaker is open")

        # Check budget
        budget_status = self.cost_tracker.get_budget_status(
            dimension="agent",
            identifier=self.config.agent_id
        )
        if budget_status["is_over_budget"]:
            is_healthy = False
            issues.append("Over budget")

        return {
            "healthy": is_healthy,
            "issues": issues,
            "timestamp": datetime.utcnow().isoformat()
        }


# ==============================================================================
# Demonstration: Side-by-Side Comparison
# ==============================================================================

async def run_comparison():
    """Run side-by-side comparison of basic vs production agent."""

    print("=" * 80)
    print("AGENT IMPROVEMENT COMPARISON")
    print("=" * 80)
    print()

    # Test tasks
    tasks = [
        "Analyze customer feedback sentiment",
        "Generate product description",
        "Summarize meeting notes"
    ]

    # ==============================================================================
    # Run BEFORE: Basic Agent
    # ==============================================================================
    print("BEFORE: Basic Agent (No Improvements)")
    print("-" * 80)

    basic_agent = BasicAgent("basic-agent-001")
    basic_start = time.time()
    basic_results = []

    for task in tasks:
        try:
            result = basic_agent.process_task(task)
            basic_results.append(result)
            print(f"✓ Task completed: {task[:50]}...")
        except Exception as e:
            print(f"✗ Task failed: {str(e)}")

    basic_duration = time.time() - basic_start
    basic_stats = basic_agent.get_stats()

    print(f"\nBasic Agent Stats:")
    print(f"  Calls: {basic_stats['call_count']}")
    print(f"  Duration: {basic_duration:.2f}s")
    print(f"  Cost tracking: ✗ Not available")
    print(f"  Error handling: ✗ Not available")
    print(f"  Memory: ✗ Not available")
    print(f"  Metrics: ✗ Not available")
    print()

    # ==============================================================================
    # Run AFTER: Production Agent
    # ==============================================================================
    print("\nAFTER: Production Agent (All 7 Improvements)")
    print("-" * 80)

    # Initialize shared infrastructure
    logger = AgentLogger(agent_id="prod-agent-001", log_level="WARNING")
    metrics = AgentMetrics(namespace="demo", subsystem="production")
    cost_tracker = CostTracker(enable_alerts=True)
    broker = MessageBroker(enable_persistence=False)

    # Create production agent
    config = AgentConfig(
        agent_id="prod-agent-001",
        model_name="gpt-4-turbo",
        enable_caching=True,
        enable_memory=True,
        cost_budget_usd=10.0
    )

    prod_agent = ProductionAgent(
        config=config,
        logger=logger,
        metrics=metrics,
        cost_tracker=cost_tracker,
        message_broker=broker
    )

    # Start session
    session_id = await prod_agent.start_session()
    print(f"Session started: {session_id}")
    print()

    prod_start = time.time()
    prod_results = []

    for i, task in enumerate(tasks):
        print(f"Processing task {i+1}/{len(tasks)}: {task[:50]}...")
        result = await prod_agent.process_task(task, priority="high")
        prod_results.append(result)

        if result["success"]:
            print(f"  ✓ Success")
            print(f"    Duration: {result['metrics']['duration_ms']:.1f}ms")
            print(f"    Cost: ${result['metrics']['cost_usd']:.6f}")
            print(f"    Quality: {result['metrics']['quality_score']:.2f}")
        else:
            print(f"  ✗ Failed: {result['error']}")
        print()

    prod_duration = time.time() - prod_start

    # Get comprehensive stats
    prod_stats = await prod_agent.get_comprehensive_stats()
    health = await prod_agent.health_check()

    print("Production Agent Stats:")
    print("-" * 80)
    print(f"✓ Total Cost: ${prod_stats['costs']['total_cost_usd']:.6f}")
    print(f"✓ Total Tokens: {prod_stats['costs']['total_tokens']:,}")
    print(f"✓ Avg Cost/Request: ${prod_stats['costs']['avg_cost_per_request']:.6f}")
    print(f"✓ Budget Remaining: ${prod_stats['costs']['budget_remaining']:.2f}")
    print(f"✓ Budget Used: {prod_stats['costs']['budget_used_pct']:.1f}%")
    print(f"✓ Circuit Breaker: {prod_stats['reliability']['circuit_breaker_state']}")
    print(f"✓ Active Sessions: {prod_stats['memory']['active_sessions']}")
    print(f"✓ Cache Enabled: {prod_stats['performance']['cache_enabled']}")
    print(f"✓ Health Status: {'Healthy' if health['healthy'] else 'Unhealthy'}")
    print()

    # ==============================================================================
    # Comparison Summary
    # ==============================================================================
    print("=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print()

    improvements = [
        ("1. Observability", "✗ None", "✓ Structured logs, metrics, tracing"),
        ("2. Reliability", "✗ No retry/CB", "✓ Retry, circuit breaker, timeout"),
        ("3. Cost Optimization", "✗ No tracking", f"✓ ${prod_stats['costs']['total_cost_usd']:.6f} tracked"),
        ("4. Memory Management", "✗ Stateless", f"✓ {prod_stats['memory']['active_sessions']} sessions"),
        ("5. Coordination", "✗ Isolated", "✓ A2A messaging enabled"),
        ("6. Evaluation", "✗ No validation", "✓ Quality scoring"),
        ("7. Deployment", "✗ No health checks", f"✓ Health: {health['healthy']}")
    ]

    print(f"{'Improvement':<25} {'Before':<20} {'After':<40}")
    print("-" * 85)
    for improvement, before, after in improvements:
        print(f"{improvement:<25} {before:<20} {after:<40}")

    print()
    print("VALUE DELIVERED:")
    print(f"  • Cost Visibility: Now tracking ${prod_stats['costs']['total_cost_usd']:.6f}")
    print(f"  • Error Resilience: Automatic retry + circuit breaker protection")
    print(f"  • Performance: {prod_stats['costs']['total_tokens']:,} tokens monitored")
    print(f"  • Context: Session memory maintains conversation history")
    print(f"  • Quality: All responses scored for quality")
    print(f"  • Production Ready: Health checks + graceful degradation")
    print()

    return {
        "basic": basic_stats,
        "production": prod_stats,
        "basic_duration": basic_duration,
        "production_duration": prod_duration
    }


if __name__ == "__main__":
    print("\n🚀 Starting Before/After Agent Comparison...\n")
    results = asyncio.run(run_comparison())
    print("✅ Comparison complete!\n")
