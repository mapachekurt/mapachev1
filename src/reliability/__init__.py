"""Reliability patterns for fault-tolerant systems.

This module provides production-ready implementations of common reliability patterns:
- Circuit Breaker: Prevent cascading failures
- Retry: Handle transient failures with exponential backoff
- Timeout: Prevent indefinite waits
- Bulkhead: Isolate resources and prevent exhaustion
"""

from .bulkhead import Bulkhead, BulkheadError, BulkheadRegistry
from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
)
from .retry import AsyncRetry, retry, RetryError
from .timeout import timeout, TimeoutError, TimeoutManager, wait_for

__all__ = [
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerError",
    "CircuitState",
    # Retry
    "retry",
    "AsyncRetry",
    "RetryError",
    # Timeout
    "timeout",
    "TimeoutError",
    "TimeoutManager",
    "wait_for",
    # Bulkhead
    "Bulkhead",
    "BulkheadError",
    "BulkheadRegistry",
]
