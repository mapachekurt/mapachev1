"""
Example usage of the observability layer.

This script demonstrates how to use the structured logging, distributed tracing,
metrics collection, and dashboard configuration in a real agent workflow.
"""

import time
import random
from typing import Dict, Any

from structured_logging import get_logger
from distributed_tracing import get_tracer
from metrics import get_metrics
from dashboards import get_dashboard, get_all_dashboards


def simulate_agent_task(
    task_id: str,
    agent_id: str,
    task_type: str = "data_processing",
) -> Dict[str, Any]:
    """
    Simulate an agent task with full observability.

    Args:
        task_id: Unique task identifier
        agent_id: Agent identifier
        task_type: Type of task to simulate

    Returns:
        Task result dictionary
    """
    # Initialize observability components
    logger = get_logger(agent_id=agent_id, environment="production")
    tracer = get_tracer(service_name="agent-service", environment="production")
    metrics = get_metrics(namespace="agent", subsystem="workflow")

    # Log task start
    logger.log_task_start(
        task_id=task_id,
        task_type=task_type,
        priority="high",
        source="api",
    )

    # Start distributed trace
    with tracer.trace_agent_task(task_id, task_type, agent_id):
        # Track metrics
        with metrics.track_task(agent_id, task_type, task_id) as task_ctx:
            try:
                # Simulate task processing
                logger.info("Starting data validation", task_id=task_id)

                with tracer.start_span("validate_data", task_id=task_id) as span:
                    time.sleep(random.uniform(0.1, 0.5))
                    span.set_attribute("records_validated", 100)
                    logger.debug("Data validation complete", records=100)

                # Simulate LLM call
                logger.info("Calling LLM for analysis", task_id=task_id)

                with tracer.trace_llm_call(
                    model="gpt-4",
                    provider="openai",
                    prompt_tokens=150,
                ) as span:
                    time.sleep(random.uniform(0.5, 2.0))
                    completion_tokens = 75

                    # Record LLM metrics
                    metrics.record_llm_tokens(
                        agent_id=agent_id,
                        model="gpt-4",
                        prompt_tokens=150,
                        completion_tokens=completion_tokens,
                    )

                    # Record cost (GPT-4: ~$0.03/1K prompt, $0.06/1K completion)
                    cost = (150 * 0.03 / 1000) + (completion_tokens * 0.06 / 1000)
                    metrics.record_cost(agent_id, cost, "llm")

                    span.set_attribute("completion_tokens", completion_tokens)
                    span.set_attribute("cost_usd", cost)

                    logger.info(
                        "LLM call complete",
                        task_id=task_id,
                        tokens_used=150 + completion_tokens,
                        cost_usd=cost,
                    )

                # Simulate database query
                with tracer.trace_external_call(
                    service="postgres",
                    operation="query",
                    method="SELECT",
                ) as span:
                    time.sleep(random.uniform(0.05, 0.2))
                    span.set_attribute("rows_returned", 42)

                # Simulate random error (10% chance)
                if random.random() < 0.1:
                    raise ValueError("Simulated processing error")

                # Task completed successfully
                duration_ms = (time.time() - task_ctx["start_time"]) * 1000
                logger.log_task_end(
                    task_id=task_id,
                    task_type=task_type,
                    success=True,
                    duration_ms=duration_ms,
                )

                logger.log_agent_action(
                    action="task_completed",
                    task_id=task_id,
                    result="success",
                )

                return {
                    "task_id": task_id,
                    "status": "success",
                    "duration_ms": duration_ms,
                }

            except Exception as e:
                # Log error
                logger.error(
                    "Task failed",
                    task_id=task_id,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                logger.exception("Task exception details", task_id=task_id)

                # Record error metric
                metrics.record_error(agent_id, type(e).__name__)

                # Re-raise
                raise


def simulate_agent_fleet() -> None:
    """Simulate multiple agents processing tasks."""
    logger = get_logger(environment="production")
    metrics = get_metrics(namespace="agent", subsystem="fleet")

    logger.info("Starting agent fleet simulation")

    agent_ids = [f"agent-{i:03d}" for i in range(1, 6)]
    task_types = ["data_processing", "analysis", "reporting", "validation"]

    for i in range(20):
        agent_id = random.choice(agent_ids)
        task_type = random.choice(task_types)
        task_id = f"task-{i:04d}"

        try:
            # Update queue depth
            metrics.set_queue_depth(agent_id, "main_queue", random.randint(0, 50))

            # Update memory usage (simulate 100-500 MB)
            memory_bytes = random.randint(100, 500) * 1024 * 1024
            metrics.set_memory_usage(agent_id, memory_bytes)

            # Process task
            result = simulate_agent_task(task_id, agent_id, task_type)
            logger.info("Fleet task completed", **result)

        except Exception as e:
            logger.warning(f"Fleet task failed: {e}", task_id=task_id)

        # Small delay between tasks
        time.sleep(0.1)

    logger.info("Agent fleet simulation complete")


def demonstrate_dashboard_export() -> None:
    """Demonstrate dashboard configuration export."""
    logger = get_logger()

    logger.info("Exporting dashboard configurations")

    # Get all dashboards
    dashboards = get_all_dashboards()

    for name, dashboard in dashboards.items():
        logger.info(
            "Dashboard available",
            name=name,
            description=dashboard.description,
            panels=len(dashboard.panels),
        )

    # Get specific dashboard
    overview_dashboard = get_dashboard("overview")
    if overview_dashboard:
        json_config = overview_dashboard.to_json()
        logger.info(
            "Overview dashboard exported",
            config_size=len(json_config),
        )

    logger.info("Dashboard export complete")


def demonstrate_context_propagation() -> None:
    """Demonstrate distributed tracing context propagation."""
    logger = get_logger(agent_id="parent-agent")
    tracer = get_tracer(service_name="parent-service")

    logger.info("Starting context propagation demo")

    # Parent operation
    with tracer.start_span("parent_operation") as parent_span:
        parent_span.set_attribute("operation", "data_ingestion")

        # Inject context for child service
        context = tracer.inject_context()
        logger.info("Context injected", context=context)

        # Simulate sending context to child service
        # In real scenario, this would be sent via HTTP headers or message metadata

        # Child operation with propagated context
        with tracer.start_span_with_context(
            "child_operation",
            context=context,
        ) as child_span:
            child_span.set_attribute("operation", "data_processing")
            time.sleep(0.2)

            logger.info("Child operation complete with parent context")

    logger.info("Context propagation demo complete")


def main() -> None:
    """Run all observability examples."""
    print("=" * 80)
    print("Observability Layer Example Usage")
    print("=" * 80)

    print("\n1. Single Task Simulation")
    print("-" * 80)
    try:
        result = simulate_agent_task("demo-task-001", "agent-demo", "demo")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Task failed (expected): {e}")

    print("\n2. Agent Fleet Simulation")
    print("-" * 80)
    simulate_agent_fleet()

    print("\n3. Dashboard Configuration Export")
    print("-" * 80)
    demonstrate_dashboard_export()

    print("\n4. Distributed Tracing Context Propagation")
    print("-" * 80)
    demonstrate_context_propagation()

    print("\n" + "=" * 80)
    print("All examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
