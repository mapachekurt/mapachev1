"""
Error Handling

Provides robust error handling utilities including:
- Retry logic with exponential backoff
- Circuit breaker pattern
- Error classification
- Graceful degradation
"""

import time
import logging
from typing import Callable, Any, Optional, Type
from functools import wraps
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories"""
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    INTERNAL = "internal"
    EXTERNAL = "external"


@dataclass
class AgentError(Exception):
    """Base exception for agent errors"""
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    retryable: bool = True
    details: dict = None

    def __str__(self):
        return f"{self.category.value}: {self.message}"


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.

    Prevents cascading failures by failing fast when error rate is high.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception,
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type that triggers the circuit
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call function through circuit breaker.

        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If circuit is open or function raises
        """
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise AgentError(
                    message="Circuit breaker is open",
                    category=ErrorCategory.INTERNAL,
                    severity=ErrorSeverity.HIGH,
                    retryable=False,
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit"""
        if self.last_failure_time is None:
            return False

        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.recovery_timeout

    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures"
            )


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        exceptions: Tuple of exceptions to catch and retry

    Example:
        @retry_with_backoff(max_attempts=3, initial_delay=2.0)
        def fetch_data():
            # code that might fail
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = initial_delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    attempt += 1

                    if attempt >= max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts"
                        )
                        raise

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}. "
                        f"Retrying in {delay:.2f}s... Error: {str(e)}"
                    )

                    time.sleep(delay)

                    # Calculate next delay with exponential backoff
                    delay = min(delay * exponential_base, max_delay)

        return wrapper

    return decorator


def graceful_degradation(fallback_value: Any = None):
    """
    Decorator for graceful degradation.

    If function fails, return fallback value instead of raising exception.

    Args:
        fallback_value: Value to return on failure

    Example:
        @graceful_degradation(fallback_value=[])
        def get_recommendations():
            # code that might fail
            return recommendations
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(
                    f"Function {func.__name__} failed, using fallback value. Error: {str(e)}"
                )
                return fallback_value

        return wrapper

    return decorator


def classify_error(error: Exception) -> tuple[ErrorCategory, ErrorSeverity]:
    """
    Classify an error by category and severity.

    Args:
        error: Exception to classify

    Returns:
        Tuple of (ErrorCategory, ErrorSeverity)
    """
    error_str = str(error).lower()

    # Network errors
    if any(keyword in error_str for keyword in ["connection", "network", "timeout"]):
        return ErrorCategory.NETWORK, ErrorSeverity.MEDIUM

    # Authentication errors
    if any(keyword in error_str for keyword in ["auth", "unauthorized", "forbidden"]):
        return ErrorCategory.AUTHENTICATION, ErrorSeverity.HIGH

    # Not found errors
    if "not found" in error_str or "404" in error_str:
        return ErrorCategory.NOT_FOUND, ErrorSeverity.LOW

    # Validation errors
    if any(keyword in error_str for keyword in ["validation", "invalid", "bad request"]):
        return ErrorCategory.VALIDATION, ErrorSeverity.LOW

    # Default: internal error
    return ErrorCategory.INTERNAL, ErrorSeverity.MEDIUM


def handle_agent_error(error: Exception, agent_name: str, operation: str) -> dict:
    """
    Handle an agent error and return error response.

    Args:
        error: Exception that occurred
        agent_name: Name of the agent
        operation: Operation that failed

    Returns:
        Error response dictionary
    """
    category, severity = classify_error(error)

    error_response = {
        "error": True,
        "agent": agent_name,
        "operation": operation,
        "message": str(error),
        "category": category.value,
        "severity": severity.value,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # Log based on severity
    if severity == ErrorSeverity.CRITICAL:
        logger.critical(f"Critical error in {agent_name}: {error}", exc_info=True)
    elif severity == ErrorSeverity.HIGH:
        logger.error(f"Error in {agent_name}: {error}", exc_info=True)
    elif severity == ErrorSeverity.MEDIUM:
        logger.warning(f"Warning in {agent_name}: {error}")
    else:
        logger.info(f"Low severity error in {agent_name}: {error}")

    return error_response


# Example usage
if __name__ == "__main__":
    # Retry example
    @retry_with_backoff(max_attempts=3, initial_delay=1.0)
    def unreliable_function():
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure")
        return "Success!"

    # Circuit breaker example
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10.0)

    def protected_operation():
        return breaker.call(unreliable_function)

    # Graceful degradation example
    @graceful_degradation(fallback_value={"status": "unavailable"})
    def get_agent_status():
        raise ConnectionError("Agent unavailable")

    print("Testing graceful degradation:", get_agent_status())

    # Error classification example
    try:
        raise ValueError("Authentication failed")
    except Exception as e:
        category, severity = classify_error(e)
        print(f"Error classified as: {category.value} with severity: {severity.value}")
