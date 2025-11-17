"""
Metrics collection and monitoring for agent operations.

This module provides Prometheus-compatible metrics collection for tracking
agent performance, resource utilization, and operational health.
"""

import time
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional
from datetime import datetime

try:
    from prometheus_client import (
        Counter,
        Histogram,
        Gauge,
        Info,
        Summary,
        CollectorRegistry,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    Counter = Any  # type: ignore
    Histogram = Any  # type: ignore
    Gauge = Any  # type: ignore


class MockMetric:
    """Mock metric implementation when Prometheus client is not available."""

    def __init__(self, name: str, documentation: str, labelnames: tuple = ()):
        self.name = name
        self.documentation = documentation
        self.labelnames = labelnames
        self._values: Dict[tuple, float] = {}

    def labels(self, **labels: str) -> "MockMetric":
        """Return a labeled version of this metric."""
        return self

    def inc(self, amount: float = 1.0) -> None:
        """Increment the metric."""
        pass

    def dec(self, amount: float = 1.0) -> None:
        """Decrement the metric."""
        pass

    def set(self, value: float) -> None:
        """Set the metric to a specific value."""
        pass

    def observe(self, amount: float) -> None:
        """Observe a value (for histograms and summaries)."""
        pass

    def time(self) -> "MockMetric":
        """Return self for context manager timing."""
        return self

    def __enter__(self) -> "MockMetric":
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        duration = time.time() - self._start_time
        self.observe(duration)


class AgentMetrics:
    """
    Prometheus metrics collection for agent operations.

    Provides comprehensive metrics tracking for agent requests, durations,
    costs, errors, and resource utilization.

    Attributes:
        registry: Prometheus collector registry
        requests_total: Counter for total requests
        duration_seconds: Histogram for request durations
        cost_usd: Counter for accumulated costs
        active_requests: Gauge for currently active requests
        errors_total: Counter for total errors
        llm_tokens_total: Counter for LLM token usage
        task_duration_seconds: Histogram for task durations

    Example:
        >>> metrics = AgentMetrics(namespace="agent", subsystem="workflow")
        >>> metrics.requests_total.labels(agent_id="agent-1", status="success").inc()
        >>> with metrics.track_request(agent_id="agent-1"):
        ...     # Automatically tracks duration and active requests
        ...     process_task()
        >>> metrics.record_cost(agent_id="agent-1", cost_usd=0.05)
    """

    def __init__(
        self,
        namespace: str = "agent",
        subsystem: str = "system",
        registry: Optional[Any] = None,
    ) -> None:
        """
        Initialize AgentMetrics with Prometheus collectors.

        Args:
            namespace: Metric namespace prefix
            subsystem: Metric subsystem prefix
            registry: Optional custom Prometheus registry
        """
        self.namespace = namespace
        self.subsystem = subsystem

        if PROMETHEUS_AVAILABLE:
            self.registry = registry or CollectorRegistry()
            self._init_prometheus_metrics()
        else:
            self.registry = None
            self._init_mock_metrics()

    def _init_prometheus_metrics(self) -> None:
        """Initialize Prometheus metric collectors."""
        if not PROMETHEUS_AVAILABLE:
            return

        # Counter: Total requests by agent and status
        self.requests_total = Counter(
            name=f"{self.namespace}_{self.subsystem}_requests_total",
            documentation="Total number of agent requests",
            labelnames=["agent_id", "task_type", "status"],
            registry=self.registry,
        )

        # Histogram: Request duration distribution
        self.duration_seconds = Histogram(
            name=f"{self.namespace}_{self.subsystem}_duration_seconds",
            documentation="Agent request duration in seconds",
            labelnames=["agent_id", "task_type"],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0),
            registry=self.registry,
        )

        # Counter: Accumulated costs in USD
        self.cost_usd = Counter(
            name=f"{self.namespace}_{self.subsystem}_cost_usd_total",
            documentation="Total cost in USD for agent operations",
            labelnames=["agent_id", "cost_type"],
            registry=self.registry,
        )

        # Gauge: Currently active requests
        self.active_requests = Gauge(
            name=f"{self.namespace}_{self.subsystem}_active_requests",
            documentation="Number of currently active requests",
            labelnames=["agent_id"],
            registry=self.registry,
        )

        # Counter: Total errors by type
        self.errors_total = Counter(
            name=f"{self.namespace}_{self.subsystem}_errors_total",
            documentation="Total number of errors",
            labelnames=["agent_id", "error_type"],
            registry=self.registry,
        )

        # Counter: LLM token usage
        self.llm_tokens_total = Counter(
            name=f"{self.namespace}_{self.subsystem}_llm_tokens_total",
            documentation="Total LLM tokens consumed",
            labelnames=["agent_id", "model", "token_type"],
            registry=self.registry,
        )

        # Histogram: Task-specific duration tracking
        self.task_duration_seconds = Histogram(
            name=f"{self.namespace}_{self.subsystem}_task_duration_seconds",
            documentation="Task execution duration in seconds",
            labelnames=["agent_id", "task_type", "status"],
            buckets=(0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0),
            registry=self.registry,
        )

        # Gauge: Queue depth
        self.queue_depth = Gauge(
            name=f"{self.namespace}_{self.subsystem}_queue_depth",
            documentation="Number of tasks in queue",
            labelnames=["agent_id", "queue_name"],
            registry=self.registry,
        )

        # Summary: Response times percentiles
        self.response_time_seconds = Summary(
            name=f"{self.namespace}_{self.subsystem}_response_time_seconds",
            documentation="Response time in seconds",
            labelnames=["agent_id", "endpoint"],
            registry=self.registry,
        )

        # Gauge: Memory usage in bytes
        self.memory_usage_bytes = Gauge(
            name=f"{self.namespace}_{self.subsystem}_memory_usage_bytes",
            documentation="Memory usage in bytes",
            labelnames=["agent_id"],
            registry=self.registry,
        )

    def _init_mock_metrics(self) -> None:
        """Initialize mock metrics when Prometheus is not available."""
        self.requests_total = MockMetric(
            "requests_total",
            "Total requests",
            ("agent_id", "task_type", "status"),
        )
        self.duration_seconds = MockMetric(
            "duration_seconds",
            "Request duration",
            ("agent_id", "task_type"),
        )
        self.cost_usd = MockMetric(
            "cost_usd",
            "Cost in USD",
            ("agent_id", "cost_type"),
        )
        self.active_requests = MockMetric(
            "active_requests",
            "Active requests",
            ("agent_id",),
        )
        self.errors_total = MockMetric(
            "errors_total",
            "Total errors",
            ("agent_id", "error_type"),
        )
        self.llm_tokens_total = MockMetric(
            "llm_tokens_total",
            "LLM tokens",
            ("agent_id", "model", "token_type"),
        )
        self.task_duration_seconds = MockMetric(
            "task_duration_seconds",
            "Task duration",
            ("agent_id", "task_type", "status"),
        )
        self.queue_depth = MockMetric(
            "queue_depth",
            "Queue depth",
            ("agent_id", "queue_name"),
        )
        self.response_time_seconds = MockMetric(
            "response_time_seconds",
            "Response time",
            ("agent_id", "endpoint"),
        )
        self.memory_usage_bytes = MockMetric(
            "memory_usage_bytes",
            "Memory usage",
            ("agent_id",),
        )

    @contextmanager
    def track_request(
        self,
        agent_id: str,
        task_type: str = "default",
    ) -> Generator[None, None, None]:
        """
        Context manager to automatically track request metrics.

        Tracks duration, active requests, and success/failure status.

        Args:
            agent_id: Unique agent identifier
            task_type: Type of task being performed

        Yields:
            None

        Example:
            >>> with metrics.track_request(agent_id="agent-1", task_type="processing"):
            ...     result = process_data()
        """
        # Increment active requests
        self.active_requests.labels(agent_id=agent_id).inc()

        start_time = time.time()
        status = "success"

        try:
            yield
        except Exception:
            status = "error"
            raise
        finally:
            # Record duration
            duration = time.time() - start_time
            self.duration_seconds.labels(
                agent_id=agent_id,
                task_type=task_type,
            ).observe(duration)

            # Increment request counter
            self.requests_total.labels(
                agent_id=agent_id,
                task_type=task_type,
                status=status,
            ).inc()

            # Decrement active requests
            self.active_requests.labels(agent_id=agent_id).dec()

    @contextmanager
    def track_task(
        self,
        agent_id: str,
        task_type: str,
        task_id: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Context manager to track task execution with detailed metrics.

        Args:
            agent_id: Unique agent identifier
            task_type: Type of task being performed
            task_id: Optional unique task identifier

        Yields:
            Dictionary for adding custom metrics during task execution

        Example:
            >>> with metrics.track_task("agent-1", "data_processing") as task_ctx:
            ...     result = process()
            ...     task_ctx["records_processed"] = len(result)
        """
        start_time = time.time()
        status = "success"
        task_context: Dict[str, Any] = {
            "task_id": task_id,
            "start_time": start_time,
        }

        try:
            yield task_context
        except Exception as e:
            status = "error"
            self.errors_total.labels(
                agent_id=agent_id,
                error_type=type(e).__name__,
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            self.task_duration_seconds.labels(
                agent_id=agent_id,
                task_type=task_type,
                status=status,
            ).observe(duration)

    def record_cost(
        self,
        agent_id: str,
        cost_usd: float,
        cost_type: str = "llm",
    ) -> None:
        """
        Record a cost metric.

        Args:
            agent_id: Unique agent identifier
            cost_usd: Cost amount in USD
            cost_type: Type of cost (e.g., "llm", "compute", "storage")

        Example:
            >>> metrics.record_cost("agent-1", 0.05, "llm")
        """
        self.cost_usd.labels(
            agent_id=agent_id,
            cost_type=cost_type,
        ).inc(cost_usd)

    def record_llm_tokens(
        self,
        agent_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        """
        Record LLM token usage.

        Args:
            agent_id: Unique agent identifier
            model: Name of the LLM model
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Example:
            >>> metrics.record_llm_tokens("agent-1", "gpt-4", 100, 50)
        """
        self.llm_tokens_total.labels(
            agent_id=agent_id,
            model=model,
            token_type="prompt",
        ).inc(prompt_tokens)

        self.llm_tokens_total.labels(
            agent_id=agent_id,
            model=model,
            token_type="completion",
        ).inc(completion_tokens)

    def record_error(
        self,
        agent_id: str,
        error_type: str,
        count: int = 1,
    ) -> None:
        """
        Record an error occurrence.

        Args:
            agent_id: Unique agent identifier
            error_type: Type or name of the error
            count: Number of errors to record (default: 1)

        Example:
            >>> metrics.record_error("agent-1", "TimeoutError")
        """
        self.errors_total.labels(
            agent_id=agent_id,
            error_type=error_type,
        ).inc(count)

    def set_queue_depth(
        self,
        agent_id: str,
        queue_name: str,
        depth: int,
    ) -> None:
        """
        Set the current queue depth.

        Args:
            agent_id: Unique agent identifier
            queue_name: Name of the queue
            depth: Current number of items in queue

        Example:
            >>> metrics.set_queue_depth("agent-1", "tasks", 42)
        """
        self.queue_depth.labels(
            agent_id=agent_id,
            queue_name=queue_name,
        ).set(depth)

    def set_memory_usage(
        self,
        agent_id: str,
        bytes_used: int,
    ) -> None:
        """
        Set the current memory usage.

        Args:
            agent_id: Unique agent identifier
            bytes_used: Memory usage in bytes

        Example:
            >>> metrics.set_memory_usage("agent-1", 1024*1024*512)  # 512 MB
        """
        self.memory_usage_bytes.labels(agent_id=agent_id).set(bytes_used)

    def get_metrics_output(self) -> bytes:
        """
        Generate Prometheus metrics output.

        Returns:
            Prometheus metrics in text format

        Example:
            >>> output = metrics.get_metrics_output()
            >>> # Serve at /metrics endpoint
        """
        if PROMETHEUS_AVAILABLE and self.registry:
            return generate_latest(self.registry)
        return b"# Prometheus client not available\n"

    def get_metrics_content_type(self) -> str:
        """
        Get the content type for metrics output.

        Returns:
            Content type string for HTTP response
        """
        if PROMETHEUS_AVAILABLE:
            return CONTENT_TYPE_LATEST
        return "text/plain"


def get_metrics(
    namespace: str = "agent",
    subsystem: str = "system",
) -> AgentMetrics:
    """
    Factory function to create a configured AgentMetrics instance.

    Args:
        namespace: Metric namespace prefix
        subsystem: Metric subsystem prefix

    Returns:
        Configured AgentMetrics instance
    """
    return AgentMetrics(namespace=namespace, subsystem=subsystem)
