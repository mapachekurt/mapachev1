"""Circuit Breaker pattern implementation for fault tolerance.

The circuit breaker prevents cascading failures by monitoring failures and
temporarily blocking calls when a failure threshold is exceeded.
"""

import asyncio
import time
from enum import Enum
from typing import Any, Callable, Optional, TypeVar
from dataclasses import dataclass


T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation, requests pass through
    OPEN = "open"  # Failures exceeded threshold, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""

    failure_threshold: int = 5  # Number of failures before opening
    success_threshold: int = 2  # Number of successes to close from half-open
    timeout: float = 60.0  # Seconds to wait before half-open
    half_open_max_calls: int = 1  # Max concurrent calls in half-open state


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""

    pass


class CircuitBreaker:
    """Circuit breaker for preventing cascading failures.

    The circuit breaker monitors failures and transitions between states:
    - CLOSED: Normal operation, all calls pass through
    - OPEN: Too many failures, calls are blocked
    - HALF_OPEN: Testing recovery, limited calls allowed

    Example:
        ```python
        cb = CircuitBreaker(failure_threshold=3, timeout=30)

        async def make_request():
            if cb.is_open():
                raise CircuitBreakerError("Circuit is open")

            try:
                result = await cb.call(external_service_call)
                return result
            except Exception as e:
                raise
        ```
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
        half_open_max_calls: int = 1,
    ):
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            success_threshold: Successes needed to close from half-open
            timeout: Seconds before attempting recovery (half-open)
            half_open_max_calls: Max concurrent calls in half-open state
        """
        self.config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout,
            half_open_max_calls=half_open_max_calls,
        )

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._half_open_calls = 0
        self._lock = asyncio.Lock()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state."""
        return self._state

    def is_open(self) -> bool:
        """Check if circuit is open (blocking calls).

        Returns:
            True if circuit is open, False otherwise
        """
        self._update_state()
        return self._state == CircuitState.OPEN

    def is_closed(self) -> bool:
        """Check if circuit is closed (normal operation).

        Returns:
            True if circuit is closed, False otherwise
        """
        self._update_state()
        return self._state == CircuitState.CLOSED

    def is_half_open(self) -> bool:
        """Check if circuit is half-open (testing recovery).

        Returns:
            True if circuit is half-open, False otherwise
        """
        self._update_state()
        return self._state == CircuitState.HALF_OPEN

    async def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function through circuit breaker.

        Args:
            func: Function to execute (can be sync or async)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            CircuitBreakerError: If circuit is open
            Exception: Any exception from func
        """
        async with self._lock:
            self._update_state()

            if self._state == CircuitState.OPEN:
                raise CircuitBreakerError(
                    f"Circuit breaker is open. "
                    f"Retry after {self.config.timeout} seconds."
                )

            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self.config.half_open_max_calls:
                    raise CircuitBreakerError(
                        "Circuit breaker is half-open with max calls reached"
                    )
                self._half_open_calls += 1

        try:
            # Execute function (handle both sync and async)
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            await self.record_success()
            return result

        except Exception as e:
            await self.record_failure()
            raise

        finally:
            if self._state == CircuitState.HALF_OPEN:
                async with self._lock:
                    self._half_open_calls -= 1

    async def record_success(self) -> None:
        """Record successful call and update state."""
        async with self._lock:
            self._failure_count = 0

            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.config.success_threshold:
                    self._transition_to_closed()

    async def record_failure(self) -> None:
        """Record failed call and update state."""
        async with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                self._transition_to_open()
            elif self._failure_count >= self.config.failure_threshold:
                self._transition_to_open()

    def _update_state(self) -> None:
        """Update state based on timeout (OPEN -> HALF_OPEN)."""
        if self._state == CircuitState.OPEN:
            if self._last_failure_time is not None:
                elapsed = time.time() - self._last_failure_time
                if elapsed >= self.config.timeout:
                    self._transition_to_half_open()

    def _transition_to_closed(self) -> None:
        """Transition to CLOSED state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._half_open_calls = 0

    def _transition_to_open(self) -> None:
        """Transition to OPEN state."""
        self._state = CircuitState.OPEN
        self._success_count = 0
        self._half_open_calls = 0

    def _transition_to_half_open(self) -> None:
        """Transition to HALF_OPEN state."""
        self._state = CircuitState.HALF_OPEN
        self._success_count = 0
        self._half_open_calls = 0

    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = None
        self._half_open_calls = 0

    def __repr__(self) -> str:
        """String representation of circuit breaker."""
        return (
            f"CircuitBreaker(state={self._state.value}, "
            f"failures={self._failure_count}, "
            f"successes={self._success_count})"
        )
