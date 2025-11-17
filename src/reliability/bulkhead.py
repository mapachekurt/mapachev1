"""Bulkhead pattern for resource isolation and preventing resource exhaustion."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional, TypeVar
import logging


logger = logging.getLogger(__name__)

T = TypeVar("T")


class BulkheadError(Exception):
    """Raised when bulkhead capacity is exceeded."""

    pass


class Bulkhead:
    """Bulkhead pattern for isolating resources and preventing exhaustion.

    Uses ThreadPoolExecutor to limit concurrent execution and prevent
    resource exhaustion. Each bulkhead maintains its own isolated pool
    of workers.

    Example:
        ```python
        # Create bulkhead with 5 max workers
        bulkhead = Bulkhead(max_workers=5)

        # Execute function in isolated pool
        result = await bulkhead.execute(cpu_intensive_task, data)

        # Check capacity
        if bulkhead.available_capacity() > 0:
            result = await bulkhead.execute(another_task)
        ```
    """

    def __init__(
        self,
        max_workers: int = 10,
        queue_size: Optional[int] = None,
        name: Optional[str] = None,
    ):
        """Initialize bulkhead.

        Args:
            max_workers: Maximum concurrent workers
            queue_size: Maximum queue size (None for unlimited)
            name: Optional name for this bulkhead
        """
        self.max_workers = max_workers
        self.queue_size = queue_size
        self.name = name or f"bulkhead-{id(self)}"

        self._executor: Optional[ThreadPoolExecutor] = None
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._active_tasks = 0
        self._total_executions = 0
        self._failed_executions = 0
        self._lock = asyncio.Lock()

    def get_pool(self) -> ThreadPoolExecutor:
        """Get or create the thread pool executor.

        Returns:
            ThreadPoolExecutor instance
        """
        if self._executor is None:
            self._executor = ThreadPoolExecutor(
                max_workers=self.max_workers,
                thread_name_prefix=f"{self.name}-worker",
            )
            logger.info(
                f"Created thread pool for {self.name} "
                f"with {self.max_workers} workers"
            )
        return self._executor

    def _get_semaphore(self) -> asyncio.Semaphore:
        """Get or create the semaphore for queue management.

        Returns:
            Asyncio semaphore
        """
        if self._semaphore is None:
            limit = self.queue_size if self.queue_size else self.max_workers * 2
            self._semaphore = asyncio.Semaphore(limit)
        return self._semaphore

    async def execute(
        self,
        func: Callable[..., T],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Execute function in isolated thread pool.

        Args:
            func: Function to execute (can be sync or async)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from func

        Raises:
            BulkheadError: If queue is full
            Exception: Any exception from func
        """
        semaphore = self._get_semaphore()

        # Check if we can acquire semaphore (non-blocking)
        if self.queue_size and semaphore.locked():
            raise BulkheadError(
                f"Bulkhead {self.name} queue is full "
                f"(max: {self.queue_size})"
            )

        async with semaphore:
            async with self._lock:
                self._active_tasks += 1
                self._total_executions += 1

            try:
                if asyncio.iscoroutinefunction(func):
                    # Async function - run directly
                    result = await func(*args, **kwargs)
                else:
                    # Sync function - run in thread pool
                    loop = asyncio.get_event_loop()
                    executor = self.get_pool()
                    result = await loop.run_in_executor(
                        executor,
                        lambda: func(*args, **kwargs),
                    )

                return result

            except Exception as e:
                async with self._lock:
                    self._failed_executions += 1
                logger.error(
                    f"Execution failed in {self.name}: {e}",
                    exc_info=True,
                )
                raise

            finally:
                async with self._lock:
                    self._active_tasks -= 1

    def available_capacity(self) -> int:
        """Get number of available worker slots.

        Returns:
            Number of available slots
        """
        return max(0, self.max_workers - self._active_tasks)

    def is_full(self) -> bool:
        """Check if bulkhead is at capacity.

        Returns:
            True if at capacity, False otherwise
        """
        return self._active_tasks >= self.max_workers

    def get_stats(self) -> Dict[str, Any]:
        """Get bulkhead statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            "name": self.name,
            "max_workers": self.max_workers,
            "active_tasks": self._active_tasks,
            "available_capacity": self.available_capacity(),
            "total_executions": self._total_executions,
            "failed_executions": self._failed_executions,
            "success_rate": (
                (self._total_executions - self._failed_executions)
                / self._total_executions
                if self._total_executions > 0
                else 0.0
            ),
        }

    async def shutdown(self, wait: bool = True) -> None:
        """Shutdown the bulkhead and cleanup resources.

        Args:
            wait: Wait for pending tasks to complete
        """
        if self._executor:
            logger.info(f"Shutting down bulkhead {self.name}")
            self._executor.shutdown(wait=wait)
            self._executor = None

    def __repr__(self) -> str:
        """String representation of bulkhead."""
        return (
            f"Bulkhead(name={self.name}, "
            f"max_workers={self.max_workers}, "
            f"active={self._active_tasks})"
        )

    async def __aenter__(self) -> "Bulkhead":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.shutdown(wait=True)


class BulkheadRegistry:
    """Registry for managing multiple named bulkheads.

    Useful for organizing bulkheads by resource type or service.

    Example:
        ```python
        registry = BulkheadRegistry()

        # Create bulkheads for different services
        registry.create("database", max_workers=5)
        registry.create("api", max_workers=10)
        registry.create("cache", max_workers=3)

        # Use bulkheads
        db_bulkhead = registry.get("database")
        result = await db_bulkhead.execute(query_database, sql)
        ```
    """

    def __init__(self):
        """Initialize bulkhead registry."""
        self._bulkheads: Dict[str, Bulkhead] = {}
        self._lock = asyncio.Lock()

    async def create(
        self,
        name: str,
        max_workers: int = 10,
        queue_size: Optional[int] = None,
    ) -> Bulkhead:
        """Create and register a new bulkhead.

        Args:
            name: Unique name for the bulkhead
            max_workers: Maximum concurrent workers
            queue_size: Maximum queue size

        Returns:
            Created bulkhead instance

        Raises:
            ValueError: If bulkhead with name already exists
        """
        async with self._lock:
            if name in self._bulkheads:
                raise ValueError(f"Bulkhead {name} already exists")

            bulkhead = Bulkhead(
                max_workers=max_workers,
                queue_size=queue_size,
                name=name,
            )
            self._bulkheads[name] = bulkhead
            logger.info(f"Registered bulkhead: {name}")
            return bulkhead

    def get(self, name: str) -> Bulkhead:
        """Get bulkhead by name.

        Args:
            name: Bulkhead name

        Returns:
            Bulkhead instance

        Raises:
            KeyError: If bulkhead not found
        """
        if name not in self._bulkheads:
            raise KeyError(f"Bulkhead {name} not found")
        return self._bulkheads[name]

    def get_or_create(
        self,
        name: str,
        max_workers: int = 10,
        queue_size: Optional[int] = None,
    ) -> Bulkhead:
        """Get existing bulkhead or create new one.

        Args:
            name: Bulkhead name
            max_workers: Maximum workers (if creating)
            queue_size: Queue size (if creating)

        Returns:
            Bulkhead instance
        """
        if name in self._bulkheads:
            return self._bulkheads[name]

        bulkhead = Bulkhead(
            max_workers=max_workers,
            queue_size=queue_size,
            name=name,
        )
        self._bulkheads[name] = bulkhead
        logger.info(f"Created and registered bulkhead: {name}")
        return bulkhead

    async def remove(self, name: str, wait: bool = True) -> None:
        """Remove and shutdown bulkhead.

        Args:
            name: Bulkhead name
            wait: Wait for pending tasks

        Raises:
            KeyError: If bulkhead not found
        """
        async with self._lock:
            if name not in self._bulkheads:
                raise KeyError(f"Bulkhead {name} not found")

            bulkhead = self._bulkheads.pop(name)
            await bulkhead.shutdown(wait=wait)
            logger.info(f"Removed bulkhead: {name}")

    def list_bulkheads(self) -> list[str]:
        """List all registered bulkhead names.

        Returns:
            List of bulkhead names
        """
        return list(self._bulkheads.keys())

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all bulkheads.

        Returns:
            Dictionary mapping bulkhead names to their stats
        """
        return {
            name: bulkhead.get_stats()
            for name, bulkhead in self._bulkheads.items()
        }

    async def shutdown_all(self, wait: bool = True) -> None:
        """Shutdown all registered bulkheads.

        Args:
            wait: Wait for pending tasks
        """
        async with self._lock:
            for name, bulkhead in self._bulkheads.items():
                logger.info(f"Shutting down bulkhead: {name}")
                await bulkhead.shutdown(wait=wait)
            self._bulkheads.clear()
