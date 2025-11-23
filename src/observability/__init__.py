"""
Observability layer for agent systems.

This module provides comprehensive observability capabilities including:
- Structured logging with AgentLogger
- Distributed tracing with AgentTracer
- Metrics collection with AgentMetrics
- Dashboard definitions for monitoring platforms

Example:
    >>> from observability import get_logger, get_tracer, get_metrics
    >>>
    >>> # Initialize observability components
    >>> logger = get_logger(agent_id="agent-001")
    >>> tracer = get_tracer(service_name="agent-service")
    >>> metrics = get_metrics(namespace="agent")
    >>>
    >>> # Use in agent operations
    >>> logger.info("Processing task", task_id="task-123")
    >>> with tracer.start_span("process_task") as span:
    ...     with metrics.track_request(agent_id="agent-001", task_type="processing"):
    ...         # Process task
    ...         pass
"""

from .structured_logging import AgentLogger, get_logger
from .distributed_tracing import AgentTracer, get_tracer
from .metrics import AgentMetrics, get_metrics
from .dashboards import (
    DashboardDefinition,
    AgentOverviewDashboard,
    AgentPerformanceDashboard,
    LLMMetricsDashboard,
    ErrorAnalysisDashboard,
    get_dashboard,
    get_all_dashboards,
    create_looker_studio_config,
    create_grafana_config,
)

__all__ = [
    # Logging
    "AgentLogger",
    "get_logger",
    # Tracing
    "AgentTracer",
    "get_tracer",
    # Metrics
    "AgentMetrics",
    "get_metrics",
    # Dashboards
    "DashboardDefinition",
    "AgentOverviewDashboard",
    "AgentPerformanceDashboard",
    "LLMMetricsDashboard",
    "ErrorAnalysisDashboard",
    "get_dashboard",
    "get_all_dashboards",
    "create_looker_studio_config",
    "create_grafana_config",
]

__version__ = "1.0.0"
