"""
Structured logging implementation for agent observability.

This module provides a structured logging interface using structlog that enables
consistent, machine-parseable log output across all agent operations.
"""

import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    structlog = None  # type: ignore


class AgentLogger:
    """
    Structured logger for agent operations using structlog.

    Provides structured logging capabilities with automatic context injection,
    JSON formatting, and integration with standard Python logging.

    Attributes:
        logger: The underlying structlog logger instance
        context: Persistent context added to all log entries

    Example:
        >>> logger = AgentLogger(agent_id="agent-001", environment="production")
        >>> logger.info("Task started", task_id="task-123", priority="high")
        >>> logger.error("Task failed", task_id="task-123", error="Connection timeout")
    """

    def __init__(
        self,
        agent_id: Optional[str] = None,
        environment: str = "development",
        log_level: str = "INFO",
        output_format: str = "json",
    ) -> None:
        """
        Initialize the AgentLogger with configuration.

        Args:
            agent_id: Unique identifier for the agent (optional)
            environment: Deployment environment (development, staging, production)
            log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            output_format: Output format ("json" or "console")
        """
        self.agent_id = agent_id
        self.environment = environment
        self.log_level = log_level
        self.output_format = output_format
        self.context: Dict[str, Any] = {}

        if STRUCTLOG_AVAILABLE:
            self._configure_structlog()
            self.logger = structlog.get_logger()
        else:
            # Fallback to standard logging if structlog is not available
            self._configure_stdlib_logging()
            self.logger = logging.getLogger(__name__)

        # Bind initial context
        if agent_id:
            self.bind(agent_id=agent_id)
        self.bind(environment=environment)

    def _configure_structlog(self) -> None:
        """Configure structlog with processors and formatters."""
        if not STRUCTLOG_AVAILABLE:
            return

        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]

        if self.output_format == "json":
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer())

        structlog.configure(
            processors=processors,
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Configure standard logging
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, self.log_level.upper()),
        )

    def _configure_stdlib_logging(self) -> None:
        """Configure standard library logging as fallback."""
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            stream=sys.stdout,
            level=getattr(logging, self.log_level.upper()),
        )

    def bind(self, **kwargs: Any) -> "AgentLogger":
        """
        Add persistent context to all subsequent log entries.

        Args:
            **kwargs: Key-value pairs to add to the logging context

        Returns:
            Self for method chaining
        """
        self.context.update(kwargs)
        if STRUCTLOG_AVAILABLE:
            self.logger = self.logger.bind(**kwargs)
        return self

    def unbind(self, *keys: str) -> "AgentLogger":
        """
        Remove keys from the persistent context.

        Args:
            *keys: Keys to remove from the logging context

        Returns:
            Self for method chaining
        """
        for key in keys:
            self.context.pop(key, None)

        if STRUCTLOG_AVAILABLE:
            # Re-create logger with updated context
            self.logger = structlog.get_logger()
            self.logger = self.logger.bind(**self.context)

        return self

    def _format_message(self, msg: str, **kwargs: Any) -> str:
        """Format message with context for stdlib logging."""
        if not kwargs:
            return msg
        context_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        return f"{msg} {context_str}"

    def debug(self, msg: str, **kwargs: Any) -> None:
        """
        Log a debug message with optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.debug(msg, **kwargs)
        else:
            self.logger.debug(self._format_message(msg, **kwargs))

    def info(self, msg: str, **kwargs: Any) -> None:
        """
        Log an info message with optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.info(msg, **kwargs)
        else:
            self.logger.info(self._format_message(msg, **kwargs))

    def warning(self, msg: str, **kwargs: Any) -> None:
        """
        Log a warning message with optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.warning(msg, **kwargs)
        else:
            self.logger.warning(self._format_message(msg, **kwargs))

    def error(self, msg: str, **kwargs: Any) -> None:
        """
        Log an error message with optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.error(msg, **kwargs)
        else:
            self.logger.error(self._format_message(msg, **kwargs))

    def critical(self, msg: str, **kwargs: Any) -> None:
        """
        Log a critical message with optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.critical(msg, **kwargs)
        else:
            self.logger.critical(self._format_message(msg, **kwargs))

    def exception(self, msg: str, **kwargs: Any) -> None:
        """
        Log an exception with traceback and optional context.

        Args:
            msg: The log message
            **kwargs: Additional context key-value pairs
        """
        if STRUCTLOG_AVAILABLE:
            self.logger.exception(msg, **kwargs)
        else:
            self.logger.exception(self._format_message(msg, **kwargs))

    def log_task_start(self, task_id: str, task_type: str, **kwargs: Any) -> None:
        """
        Log the start of a task with standardized format.

        Args:
            task_id: Unique task identifier
            task_type: Type of task being started
            **kwargs: Additional task context
        """
        self.info(
            "Task started",
            task_id=task_id,
            task_type=task_type,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs,
        )

    def log_task_end(
        self,
        task_id: str,
        task_type: str,
        success: bool,
        duration_ms: float,
        **kwargs: Any,
    ) -> None:
        """
        Log the completion of a task with standardized format.

        Args:
            task_id: Unique task identifier
            task_type: Type of task that completed
            success: Whether the task completed successfully
            duration_ms: Task duration in milliseconds
            **kwargs: Additional task context
        """
        level = self.info if success else self.error
        level(
            "Task completed",
            task_id=task_id,
            task_type=task_type,
            success=success,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs,
        )

    def log_agent_action(
        self,
        action: str,
        agent_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Log an agent action with standardized format.

        Args:
            action: The action being performed
            agent_id: Agent identifier (uses bound agent_id if not provided)
            **kwargs: Additional action context
        """
        self.info(
            "Agent action",
            action=action,
            agent_id=agent_id or self.agent_id,
            timestamp=datetime.utcnow().isoformat(),
            **kwargs,
        )


def get_logger(
    agent_id: Optional[str] = None,
    environment: str = "development",
    log_level: str = "INFO",
) -> AgentLogger:
    """
    Factory function to create a configured AgentLogger instance.

    Args:
        agent_id: Unique identifier for the agent
        environment: Deployment environment
        log_level: Minimum log level

    Returns:
        Configured AgentLogger instance
    """
    return AgentLogger(
        agent_id=agent_id,
        environment=environment,
        log_level=log_level,
    )
