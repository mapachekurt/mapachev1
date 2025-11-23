"""
Logging Configuration

Provides structured JSON logging for all agents and services.
"""

import logging
import os
import sys
from typing import Any, Dict
import structlog
from datetime import datetime


def configure_logging(
    service_name: str,
    environment: str = None,
    log_level: str = None,
) -> None:
    """
    Configure structured logging for the service.

    Args:
        service_name: Name of the service (agent name or "registry")
        environment: Environment (development, staging, production)
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    environment = environment or os.getenv("ENVIRONMENT", "development")
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO")

    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    # Structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    # Add environment-specific processors
    if environment == "production":
        # JSON output for production
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Pretty console output for development
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Get logger and log startup
    logger = get_logger(service_name)
    logger.info(
        "logging_configured",
        service=service_name,
        environment=environment,
        log_level=log_level,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger.

    Args:
        name: Logger name (typically service or module name)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class RequestIDProcessor:
    """Add request ID to all log entries"""

    def __init__(self):
        self.request_id = None

    def __call__(self, logger, method_name, event_dict):
        if self.request_id:
            event_dict["request_id"] = self.request_id
        return event_dict


def log_agent_message(
    logger: structlog.BoundLogger,
    direction: str,
    agent_name: str,
    message: str,
    context: Dict[str, Any] = None,
):
    """
    Log an agent-to-agent message.

    Args:
        logger: Structlog logger
        direction: "sent" or "received"
        agent_name: Name of the agent
        message: Message content
        context: Additional context
    """
    logger.info(
        "agent_message",
        direction=direction,
        agent=agent_name,
        message=message,
        context=context or {},
    )


def log_performance(
    logger: structlog.BoundLogger,
    operation: str,
    duration_ms: float,
    success: bool,
    metadata: Dict[str, Any] = None,
):
    """
    Log performance metrics.

    Args:
        logger: Structlog logger
        operation: Operation name
        duration_ms: Duration in milliseconds
        success: Whether the operation succeeded
        metadata: Additional metadata
    """
    logger.info(
        "performance",
        operation=operation,
        duration_ms=duration_ms,
        success=success,
        metadata=metadata or {},
    )


def log_error(
    logger: structlog.BoundLogger,
    error: Exception,
    context: Dict[str, Any] = None,
):
    """
    Log an error with full context.

    Args:
        logger: Structlog logger
        error: Exception that occurred
        context: Additional context
    """
    logger.error(
        "error_occurred",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True,
    )


# Example usage
if __name__ == "__main__":
    configure_logging("example_service", "development", "INFO")
    logger = get_logger("example")

    logger.info("service_started", version="1.0.0")
    logger.debug("debug_message", details="some details")
    log_agent_message(logger, "sent", "agent_a", "Hello", {"to": "agent_b"})
    log_performance(logger, "process_request", 125.5, True, {"endpoint": "/test"})

    try:
        raise ValueError("Example error")
    except Exception as e:
        log_error(logger, e, {"operation": "test"})
