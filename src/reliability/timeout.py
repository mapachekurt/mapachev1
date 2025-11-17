"""Timeout pattern for preventing indefinite waits on async operations."""

import asyncio
import functools
from typing import Any, Callable, Optional, TypeVar


T = TypeVar("T")


class TimeoutError(asyncio.TimeoutError):
    """Raised when operation exceeds timeout."""

    pass


def timeout(seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for adding timeout to async functions.

    Wraps async functions with asyncio.wait_for to enforce a timeout.
    If the function doesn't complete within the specified time, raises
    TimeoutError.

    Args:
        seconds: Timeout duration in seconds

    Returns:
        Decorated function with timeout enforcement

    Raises:
        TimeoutError: If function execution exceeds timeout
        ValueError: If applied to non-async function

    Example:
        ```python
        @timeout(5.0)
        async def fetch_data():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

        # Will timeout after 5 seconds
        try:
            data = await fetch_data()
        except TimeoutError:
            print("Request timed out")
        ```
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(
                f"@timeout can only be applied to async functions. "
                f"{func.__name__} is not async."
            )

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds,
                )
                return result
            except asyncio.TimeoutError as e:
                raise TimeoutError(
                    f"{func.__name__} exceeded timeout of {seconds}s"
                ) from e

        return wrapper

    return decorator


class AsyncTimeout:
    """Async context manager for timeout enforcement.

    Provides more flexible timeout control than the decorator.
    Uses asyncio.timeout (Python 3.11+) or asyncio.wait_for.

    Example:
        ```python
        async with AsyncTimeout(5.0):
            result = await long_running_operation()
        ```
    """

    def __init__(self, seconds: float):
        """Initialize timeout context.

        Args:
            seconds: Timeout duration in seconds
        """
        self.seconds = seconds
        self._task: Optional[asyncio.Task[Any]] = None

    async def __aenter__(self) -> "AsyncTimeout":
        """Enter timeout context."""
        self._task = asyncio.current_task()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit timeout context."""
        self._task = None


async def wait_for(
    coro: Callable[..., T],
    timeout_seconds: float,
    *args: Any,
    **kwargs: Any,
) -> T:
    """Execute coroutine with timeout.

    Helper function for running async operations with timeout without
    using decorators or context managers.

    Args:
        coro: Async function to execute
        timeout_seconds: Timeout in seconds
        *args: Positional arguments for coro
        **kwargs: Keyword arguments for coro

    Returns:
        Result from coroutine

    Raises:
        TimeoutError: If execution exceeds timeout

    Example:
        ```python
        result = await wait_for(fetch_user, 5.0, user_id=123)
        ```
    """
    try:
        result = await asyncio.wait_for(
            coro(*args, **kwargs),
            timeout=timeout_seconds,
        )
        return result
    except asyncio.TimeoutError as e:
        raise TimeoutError(
            f"Operation exceeded timeout of {timeout_seconds}s"
        ) from e


class TimeoutManager:
    """Manager for multiple concurrent operations with individual timeouts.

    Useful for managing multiple async operations that each need their
    own timeout constraints.

    Example:
        ```python
        manager = TimeoutManager()

        tasks = [
            manager.run(fetch_user, 5.0, user_id=1),
            manager.run(fetch_orders, 10.0, user_id=1),
            manager.run(fetch_profile, 3.0, user_id=1),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        ```
    """

    def __init__(self):
        """Initialize timeout manager."""
        self._tasks: list[asyncio.Task[Any]] = []

    async def run(
        self,
        coro: Callable[..., T],
        timeout_seconds: float,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Run coroutine with timeout and track task.

        Args:
            coro: Async function to execute
            timeout_seconds: Timeout in seconds
            *args: Positional arguments for coro
            **kwargs: Keyword arguments for coro

        Returns:
            Result from coroutine

        Raises:
            TimeoutError: If execution exceeds timeout
        """
        task = asyncio.create_task(
            wait_for(coro, timeout_seconds, *args, **kwargs)
        )
        self._tasks.append(task)
        return await task

    async def cancel_all(self) -> None:
        """Cancel all tracked tasks."""
        for task in self._tasks:
            if not task.done():
                task.cancel()

        # Wait for all tasks to complete cancellation
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    def get_active_tasks(self) -> list[asyncio.Task[Any]]:
        """Get list of active (not done) tasks.

        Returns:
            List of active tasks
        """
        return [task for task in self._tasks if not task.done()]

    def get_completed_tasks(self) -> list[asyncio.Task[Any]]:
        """Get list of completed tasks.

        Returns:
            List of completed tasks
        """
        return [task for task in self._tasks if task.done()]
