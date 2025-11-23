"""
Distributed tracing implementation for agent operations.

This module provides distributed tracing capabilities using OpenTelemetry,
enabling end-to-end visibility across agent workflows and service boundaries.
"""

import time
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional
from datetime import datetime

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
        SpanExporter,
    )
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.trace import Status, StatusCode, Span, Tracer
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    trace = None  # type: ignore
    Span = Any  # type: ignore
    Tracer = Any  # type: ignore
    SpanExporter = Any  # type: ignore


class MockSpan:
    """Mock span implementation when OpenTelemetry is not available."""

    def __init__(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        self.name = name
        self.attributes = attributes or {}
        self.status_code = "OK"
        self.status_description = ""
        self.events: list = []
        self.start_time = time.time()
        self.end_time: Optional[float] = None

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on the span."""
        self.attributes[key] = value

    def set_status(self, status_code: str, description: str = "") -> None:
        """Set the status of the span."""
        self.status_code = status_code
        self.status_description = description

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the span."""
        self.events.append({
            "name": name,
            "attributes": attributes or {},
            "timestamp": time.time(),
        })

    def end(self) -> None:
        """End the span."""
        self.end_time = time.time()

    def __enter__(self) -> "MockSpan":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            self.set_status("ERROR", str(exc_val))
        self.end()


class AgentTracer:
    """
    Distributed tracing implementation using OpenTelemetry.

    Provides distributed tracing capabilities for tracking agent operations
    across service boundaries with context propagation.

    Attributes:
        service_name: Name of the service being traced
        tracer: The underlying OpenTelemetry tracer instance
        propagator: Context propagator for distributed tracing

    Example:
        >>> tracer = AgentTracer(service_name="agent-service")
        >>> with tracer.start_span("process_task", task_id="123") as span:
        ...     span.set_attribute("status", "processing")
        ...     # Do work
        >>> context = tracer.extract_context({"traceparent": "00-..."})
        >>> with tracer.start_span_with_context("child_task", context):
        ...     # Work with propagated context
    """

    def __init__(
        self,
        service_name: str = "agent-service",
        environment: str = "development",
        enable_console_export: bool = True,
        custom_exporter: Optional[Any] = None,
    ) -> None:
        """
        Initialize the AgentTracer with configuration.

        Args:
            service_name: Name of the service for trace identification
            environment: Deployment environment
            enable_console_export: Whether to export traces to console (for development)
            custom_exporter: Optional custom span exporter
        """
        self.service_name = service_name
        self.environment = environment
        self.enable_console_export = enable_console_export

        if OPENTELEMETRY_AVAILABLE:
            self._configure_opentelemetry(custom_exporter)
            self.tracer: Tracer = trace.get_tracer(__name__)
            self.propagator = TraceContextTextMapPropagator()
        else:
            self.tracer = None  # type: ignore
            self.propagator = None

    def _configure_opentelemetry(self, custom_exporter: Optional[SpanExporter]) -> None:
        """Configure OpenTelemetry tracing with exporters."""
        if not OPENTELEMETRY_AVAILABLE:
            return

        # Create resource with service information
        resource = Resource.create({
            "service.name": self.service_name,
            "deployment.environment": self.environment,
        })

        # Create tracer provider
        provider = TracerProvider(resource=resource)

        # Add span processors
        if self.enable_console_export:
            console_exporter = ConsoleSpanExporter()
            provider.add_span_processor(BatchSpanProcessor(console_exporter))

        if custom_exporter:
            provider.add_span_processor(BatchSpanProcessor(custom_exporter))

        # Set as global tracer provider
        trace.set_tracer_provider(provider)

    @contextmanager
    def start_span(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Generator[Any, None, None]:
        """
        Start a new tracing span as a context manager.

        Args:
            name: Name of the span
            attributes: Optional attributes to attach to the span
            **kwargs: Additional span attributes as keyword arguments

        Yields:
            The active span instance

        Example:
            >>> with tracer.start_span("database_query", db="postgres") as span:
            ...     span.set_attribute("query", "SELECT * FROM users")
            ...     result = execute_query()
        """
        combined_attributes = {**(attributes or {}), **kwargs}

        if OPENTELEMETRY_AVAILABLE and self.tracer:
            with self.tracer.start_as_current_span(name) as span:
                for key, value in combined_attributes.items():
                    span.set_attribute(key, value)
                try:
                    yield span
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        else:
            # Use mock span when OpenTelemetry is not available
            mock_span = MockSpan(name, combined_attributes)
            try:
                yield mock_span
            except Exception as e:
                mock_span.set_status("ERROR", str(e))
                raise
            finally:
                mock_span.end()

    def start_span_manual(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Start a new span that must be manually ended.

        Args:
            name: Name of the span
            attributes: Optional attributes to attach to the span

        Returns:
            The span instance (must call .end() when done)

        Example:
            >>> span = tracer.start_span_manual("long_operation")
            >>> try:
            ...     # Do work
            ...     span.set_attribute("result", "success")
            ... finally:
            ...     span.end()
        """
        if OPENTELEMETRY_AVAILABLE and self.tracer:
            span = self.tracer.start_span(name)
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)
            return span
        else:
            return MockSpan(name, attributes)

    @contextmanager
    def start_span_with_context(
        self,
        name: str,
        context: Optional[Dict[str, str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Any, None, None]:
        """
        Start a span with propagated context from a parent span.

        Args:
            name: Name of the span
            context: Propagated context dictionary (from extract_context)
            attributes: Optional attributes to attach to the span

        Yields:
            The active span instance

        Example:
            >>> # In parent service
            >>> context = tracer.inject_context()
            >>> # Send context to child service
            >>>
            >>> # In child service
            >>> with tracer.start_span_with_context("child_op", context) as span:
            ...     # Work is traced as part of parent context
        """
        if OPENTELEMETRY_AVAILABLE and self.tracer and context:
            # Extract context from carrier
            parent_context = self.propagator.extract(context)
            with self.tracer.start_as_current_span(
                name,
                context=parent_context,
            ) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)
                try:
                    yield span
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
        else:
            # Fallback to regular span
            with self.start_span(name, attributes) as span:
                yield span

    def inject_context(self) -> Dict[str, str]:
        """
        Inject current trace context into a carrier for propagation.

        Returns:
            Dictionary containing trace context for propagation

        Example:
            >>> context = tracer.inject_context()
            >>> # Send context in HTTP headers or message metadata
            >>> headers = {"traceparent": context.get("traceparent")}
        """
        if OPENTELEMETRY_AVAILABLE and self.propagator:
            carrier: Dict[str, str] = {}
            self.propagator.inject(carrier)
            return carrier
        return {}

    def extract_context(self, carrier: Dict[str, str]) -> Optional[Any]:
        """
        Extract trace context from a carrier.

        Args:
            carrier: Dictionary containing trace context (e.g., HTTP headers)

        Returns:
            Extracted context or None

        Example:
            >>> context = tracer.extract_context({"traceparent": "00-..."})
            >>> with tracer.start_span_with_context("operation", context):
            ...     # Work with parent context
        """
        if OPENTELEMETRY_AVAILABLE and self.propagator:
            return self.propagator.extract(carrier)
        return None

    def trace_agent_task(
        self,
        task_id: str,
        task_type: str,
        agent_id: Optional[str] = None,
    ) -> Any:
        """
        Create a span for an agent task with standardized attributes.

        Args:
            task_id: Unique task identifier
            task_type: Type of task being performed
            agent_id: Optional agent identifier

        Returns:
            Context manager for the task span

        Example:
            >>> with tracer.trace_agent_task("task-123", "data_processing", "agent-1"):
            ...     process_data()
        """
        attributes = {
            "task.id": task_id,
            "task.type": task_type,
            "task.start_time": datetime.utcnow().isoformat(),
        }
        if agent_id:
            attributes["agent.id"] = agent_id

        return self.start_span(f"agent_task.{task_type}", attributes=attributes)

    def trace_llm_call(
        self,
        model: str,
        provider: str,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
    ) -> Any:
        """
        Create a span for an LLM API call with standardized attributes.

        Args:
            model: Name of the LLM model
            provider: LLM provider (e.g., "openai", "anthropic")
            prompt_tokens: Number of prompt tokens (if known)
            completion_tokens: Number of completion tokens (if known)

        Returns:
            Context manager for the LLM call span

        Example:
            >>> with tracer.trace_llm_call("gpt-4", "openai") as span:
            ...     response = call_llm()
            ...     span.set_attribute("completion_tokens", len(response))
        """
        attributes = {
            "llm.model": model,
            "llm.provider": provider,
        }
        if prompt_tokens is not None:
            attributes["llm.prompt_tokens"] = prompt_tokens
        if completion_tokens is not None:
            attributes["llm.completion_tokens"] = completion_tokens

        return self.start_span("llm_call", attributes=attributes)

    def trace_external_call(
        self,
        service: str,
        operation: str,
        method: Optional[str] = None,
    ) -> Any:
        """
        Create a span for an external service call.

        Args:
            service: Name of the external service
            operation: Operation being performed
            method: HTTP method or RPC method (optional)

        Returns:
            Context manager for the external call span

        Example:
            >>> with tracer.trace_external_call("postgres", "query", "SELECT") as span:
            ...     result = db.query("SELECT * FROM users")
            ...     span.set_attribute("rows_returned", len(result))
        """
        attributes = {
            "external.service": service,
            "external.operation": operation,
        }
        if method:
            attributes["external.method"] = method

        return self.start_span(f"external.{service}", attributes=attributes)


def get_tracer(
    service_name: str = "agent-service",
    environment: str = "development",
) -> AgentTracer:
    """
    Factory function to create a configured AgentTracer instance.

    Args:
        service_name: Name of the service for trace identification
        environment: Deployment environment

    Returns:
        Configured AgentTracer instance
    """
    return AgentTracer(
        service_name=service_name,
        environment=environment,
    )
