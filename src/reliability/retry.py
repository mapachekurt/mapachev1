"""Retry pattern with exponential backoff for handling transient failures."""

import asyncio
import functools
import logging
import random
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union, cast


logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""

    def __init__(self, message: str, last_exception: Exception):
        """Initialize retry error.

        Args:
            message: Error message
            last_exception: The last exception that caused retry failure
        """
        super().__init__(message)
        self.last_exception = last_exception


def retry(
    max_attempts: int = 3,
    exponential_base: float = 2.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for retrying functions with exponential backoff.

    Retries a function when specified exceptions occur, with exponential
    backoff between attempts. Supports both sync and async functions.

    Args:
        max_attempts: Maximum number of retry attempts (including first call)
        exponential_base: Base for exponential backoff calculation
        max_delay: Maximum delay between retries in seconds
        exceptions: Tuple of exception types to catch and retry
        jitter: Add random jitter to backoff delay

    Returns:
        Decorated function with retry logic

    Example:
        ```python
        @retry(max_attempts=3, exponential_base=2.0)
        async def fetch_data():
            response = await http_client.get("/api/data")
            return response.json()

        # Retries with delays: 2^0=1s, 2^1=2s, 2^2=4s
        data = await fetch_data()
        ```
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None

                for attempt in range(1, max_attempts + 1):
                    try:
                        result = await func(*args, **kwargs)
                        if attempt > 1:
                            logger.info(
                                f"{func.__name__} succeeded on attempt {attempt}"
                            )
                        return result

                    except exceptions as e:
                        last_exception = e

                        if attempt == max_attempts:
                            logger.error(
                                f"{func.__name__} failed after {max_attempts} attempts",
                                exc_info=True,
                            )
                            raise RetryError(
                                f"Failed after {max_attempts} attempts",
                                last_exception=e,
                            ) from e

                        # Calculate exponential backoff delay
                        delay = min(
                            exponential_base ** (attempt - 1),
                            max_delay,
                        )

                        # Add jitter to prevent thundering herd
                        if jitter:
                            delay = delay * (0.5 + random.random())

                        logger.warning(
                            f"{func.__name__} attempt {attempt}/{max_attempts} "
                            f"failed: {e}. Retrying in {delay:.2f}s"
                        )

                        await asyncio.sleep(delay)

                # Should never reach here, but for type checking
                if last_exception:
                    raise last_exception
                raise RuntimeError("Unexpected retry state")

            return cast(Callable[..., T], async_wrapper)

        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception: Optional[Exception] = None

                for attempt in range(1, max_attempts + 1):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 1:
                            logger.info(
                                f"{func.__name__} succeeded on attempt {attempt}"
                            )
                        return result

                    except exceptions as e:
                        last_exception = e

                        if attempt == max_attempts:
                            logger.error(
                                f"{func.__name__} failed after {max_attempts} attempts",
                                exc_info=True,
                            )
                            raise RetryError(
                                f"Failed after {max_attempts} attempts",
                                last_exception=e,
                            ) from e

                        # Calculate exponential backoff delay
                        delay = min(
                            exponential_base ** (attempt - 1),
                            max_delay,
                        )

                        # Add jitter to prevent thundering herd
                        if jitter:
                            delay = delay * (0.5 + random.random())

                        logger.warning(
                            f"{func.__name__} attempt {attempt}/{max_attempts} "
                            f"failed: {e}. Retrying in {delay:.2f}s"
                        )

                        import time
                        time.sleep(delay)

                # Should never reach here, but for type checking
                if last_exception:
                    raise last_exception
                raise RuntimeError("Unexpected retry state")

            return cast(Callable[..., T], sync_wrapper)

    return decorator


class AsyncRetry:
    """Async context manager for retry logic with exponential backoff.

    Provides more control over retry logic compared to the decorator.

    Example:
        ```python
        retry_policy = AsyncRetry(max_attempts=5, exponential_base=2.0)

        async for attempt in retry_policy:
            async with attempt:
                result = await risky_operation()
                break  # Success, exit retry loop
        ```
    """

    def __init__(
        self,
        max_attempts: int = 3,
        exponential_base: float = 2.0,
        max_delay: float = 60.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        jitter: bool = True,
    ):
        """Initialize async retry manager.

        Args:
            max_attempts: Maximum number of retry attempts
            exponential_base: Base for exponential backoff
            max_delay: Maximum delay between retries
            exceptions: Exceptions to catch and retry
            jitter: Add random jitter to backoff
        """
        self.max_attempts = max_attempts
        self.exponential_base = exponential_base
        self.max_delay = max_delay
        self.exceptions = exceptions
        self.jitter = jitter
        self.attempt = 0
        self.last_exception: Optional[Exception] = None

    def __aiter__(self) -> "AsyncRetry":
        """Return async iterator."""
        return self

    async def __anext__(self) -> "AttemptContext":
        """Get next retry attempt.

        Returns:
            Attempt context manager

        Raises:
            StopAsyncIteration: When max attempts reached
        """
        self.attempt += 1

        if self.attempt > self.max_attempts:
            if self.last_exception:
                raise RetryError(
                    f"Failed after {self.max_attempts} attempts",
                    last_exception=self.last_exception,
                )
            raise StopAsyncIteration

        return AttemptContext(self)


class AttemptContext:
    """Context manager for a single retry attempt."""

    def __init__(self, retry: AsyncRetry):
        """Initialize attempt context.

        Args:
            retry: Parent AsyncRetry instance
        """
        self.retry = retry

    async def __aenter__(self) -> "AttemptContext":
        """Enter attempt context."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        """Exit attempt context and handle exceptions.

        Returns:
            True to suppress exception, False to propagate
        """
        if exc_type is None:
            # Success
            return True

        if not isinstance(exc_val, self.retry.exceptions):
            # Not a retryable exception
            return False

        self.retry.last_exception = exc_val  # type: ignore

        if self.retry.attempt >= self.retry.max_attempts:
            # Max attempts reached
            return False

        # Calculate backoff delay
        delay = min(
            self.retry.exponential_base ** (self.retry.attempt - 1),
            self.retry.max_delay,
        )

        if self.retry.jitter:
            delay = delay * (0.5 + random.random())

        logger.warning(
            f"Attempt {self.retry.attempt}/{self.retry.max_attempts} "
            f"failed: {exc_val}. Retrying in {delay:.2f}s"
        )

        await asyncio.sleep(delay)

        # Suppress exception to continue retry loop
        return True
