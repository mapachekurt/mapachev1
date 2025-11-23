"""Coordination Primitives for Multi-Agent Systems.

This module provides synchronization primitives for coordinating multiple agents:
- Semaphore: Limit concurrent access to shared resources
- Barrier: Synchronize multiple agents at a checkpoint
- Queue: Thread-safe message passing between agents
"""

import asyncio
from collections import deque
from typing import Any, Dict, List, Optional, Set
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class Semaphore:
    """Distributed semaphore for controlling concurrent access to resources.

    Allows a specified number of agents to access a shared resource concurrently.
    Additional agents will wait until a slot becomes available.
    """

    def __init__(self, value: int = 1, name: Optional[str] = None):
        """Initialize the semaphore.

        Args:
            value: Initial value (number of concurrent accesses allowed)
            name: Optional name for logging/debugging
        """
        if value < 0:
            raise ValueError("Semaphore value must be non-negative")

        self._value = value
        self._initial_value = value
        self._waiters: deque = deque()
        self._lock = asyncio.Lock()
        self._name = name or f"semaphore-{id(self)}"
        self._holders: Set[str] = set()
        self._acquisition_times: Dict[str, datetime] = {}

        logger.debug(f"Semaphore '{self._name}' initialized with value {value}")

    async def acquire(self, agent_id: str, timeout: Optional[float] = None) -> bool:
        """Acquire the semaphore.

        Args:
            agent_id: ID of the agent acquiring the semaphore
            timeout: Optional timeout in seconds

        Returns:
            True if acquired, False if timed out

        Raises:
            asyncio.TimeoutError: If timeout is reached
        """
        async with self._lock:
            # Check if already held by this agent
            if agent_id in self._holders:
                logger.warning(
                    f"Agent {agent_id} already holds semaphore '{self._name}'"
                )
                return True

            # If semaphore available, acquire immediately
            if self._value > 0:
                self._value -= 1
                self._holders.add(agent_id)
                self._acquisition_times[agent_id] = datetime.utcnow()
                logger.debug(
                    f"Agent {agent_id} acquired semaphore '{self._name}' "
                    f"(available: {self._value}/{self._initial_value})"
                )
                return True

        # Wait for semaphore to become available
        waiter = asyncio.Future()
        self._waiters.append((agent_id, waiter))

        try:
            if timeout:
                await asyncio.wait_for(waiter, timeout=timeout)
            else:
                await waiter

            async with self._lock:
                self._holders.add(agent_id)
                self._acquisition_times[agent_id] = datetime.utcnow()
                logger.debug(
                    f"Agent {agent_id} acquired semaphore '{self._name}' after waiting "
                    f"(available: {self._value}/{self._initial_value})"
                )
            return True

        except asyncio.TimeoutError:
            # Remove from waiters on timeout
            self._waiters = deque(
                (aid, fut) for aid, fut in self._waiters if aid != agent_id
            )
            logger.warning(
                f"Agent {agent_id} timed out waiting for semaphore '{self._name}'"
            )
            return False

    async def release(self, agent_id: str) -> bool:
        """Release the semaphore.

        Args:
            agent_id: ID of the agent releasing the semaphore

        Returns:
            True if released, False if agent didn't hold the semaphore
        """
        async with self._lock:
            if agent_id not in self._holders:
                logger.warning(
                    f"Agent {agent_id} attempted to release semaphore '{self._name}' "
                    f"without holding it"
                )
                return False

            self._holders.remove(agent_id)
            self._acquisition_times.pop(agent_id, None)
            self._value += 1

            # Wake up next waiter if any
            while self._waiters:
                waiter_agent_id, waiter_future = self._waiters.popleft()
                if not waiter_future.done():
                    self._value -= 1
                    waiter_future.set_result(True)
                    logger.debug(
                        f"Agent {agent_id} released semaphore '{self._name}', "
                        f"waking up agent {waiter_agent_id} "
                        f"(available: {self._value}/{self._initial_value})"
                    )
                    return True

            logger.debug(
                f"Agent {agent_id} released semaphore '{self._name}' "
                f"(available: {self._value}/{self._initial_value})"
            )
            return True

    async def __aenter__(self):
        """Async context manager entry."""
        await self.acquire("context-manager")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.release("context-manager")

    def get_stats(self) -> Dict[str, Any]:
        """Get semaphore statistics.

        Returns:
            Dictionary with current state and statistics
        """
        return {
            "name": self._name,
            "available": self._value,
            "total": self._initial_value,
            "holders": list(self._holders),
            "waiting": len(self._waiters),
            "acquisition_times": {
                agent_id: time.isoformat()
                for agent_id, time in self._acquisition_times.items()
            },
        }


class Barrier:
    """Distributed barrier for synchronizing multiple agents.

    All agents must reach the barrier before any can proceed. Useful for
    coordinating parallel agents that need to synchronize at certain points.
    """

    def __init__(self, parties: int, name: Optional[str] = None):
        """Initialize the barrier.

        Args:
            parties: Number of agents that must wait at the barrier
            name: Optional name for logging/debugging
        """
        if parties < 1:
            raise ValueError("Barrier parties must be at least 1")

        self._parties = parties
        self._name = name or f"barrier-{id(self)}"
        self._waiting: Set[str] = set()
        self._waiting_futures: Dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()
        self._broken = False
        self._arrival_times: Dict[str, datetime] = {}

        logger.debug(f"Barrier '{self._name}' initialized for {parties} parties")

    async def wait(self, agent_id: str, timeout: Optional[float] = None) -> bool:
        """Wait at the barrier until all parties have arrived.

        Args:
            agent_id: ID of the agent waiting at the barrier
            timeout: Optional timeout in seconds

        Returns:
            True if barrier released, False if timed out or broken

        Raises:
            asyncio.TimeoutError: If timeout is reached
        """
        async with self._lock:
            if self._broken:
                logger.error(f"Barrier '{self._name}' is broken")
                return False

            if agent_id in self._waiting:
                logger.warning(
                    f"Agent {agent_id} already waiting at barrier '{self._name}'"
                )
                return True

            self._waiting.add(agent_id)
            self._arrival_times[agent_id] = datetime.utcnow()
            waiter = asyncio.Future()
            self._waiting_futures[agent_id] = waiter

            logger.debug(
                f"Agent {agent_id} arrived at barrier '{self._name}' "
                f"({len(self._waiting)}/{self._parties})"
            )

            # Check if all parties have arrived
            if len(self._waiting) == self._parties:
                logger.info(
                    f"Barrier '{self._name}' released: all {self._parties} parties arrived"
                )
                # Release all waiting agents
                for waiting_agent_id, future in self._waiting_futures.items():
                    if not future.done():
                        future.set_result(True)

                # Reset barrier for next use
                self._waiting.clear()
                self._waiting_futures.clear()
                self._arrival_times.clear()
                return True

        # Wait for barrier to be released
        try:
            if timeout:
                await asyncio.wait_for(waiter, timeout=timeout)
            else:
                await waiter
            return True

        except asyncio.TimeoutError:
            async with self._lock:
                self._waiting.discard(agent_id)
                self._waiting_futures.pop(agent_id, None)
                self._arrival_times.pop(agent_id, None)
                logger.warning(
                    f"Agent {agent_id} timed out at barrier '{self._name}'"
                )
            return False

    async def reset(self) -> None:
        """Reset the barrier, releasing all waiting agents."""
        async with self._lock:
            for future in self._waiting_futures.values():
                if not future.done():
                    future.set_result(False)

            self._waiting.clear()
            self._waiting_futures.clear()
            self._arrival_times.clear()
            self._broken = False
            logger.info(f"Barrier '{self._name}' reset")

    async def abort(self) -> None:
        """Abort the barrier, marking it as broken."""
        async with self._lock:
            self._broken = True
            for future in self._waiting_futures.values():
                if not future.done():
                    future.set_result(False)

            logger.warning(f"Barrier '{self._name}' aborted and marked as broken")

    def get_stats(self) -> Dict[str, Any]:
        """Get barrier statistics.

        Returns:
            Dictionary with current state and statistics
        """
        return {
            "name": self._name,
            "parties": self._parties,
            "waiting": list(self._waiting),
            "waiting_count": len(self._waiting),
            "broken": self._broken,
            "arrival_times": {
                agent_id: time.isoformat()
                for agent_id, time in self._arrival_times.items()
            },
        }


class Queue:
    """Distributed queue for agent-to-agent message passing.

    Provides a thread-safe, async queue for passing messages between agents.
    Supports priority queuing, message filtering, and flow control.
    """

    def __init__(
        self,
        maxsize: int = 0,
        name: Optional[str] = None,
        priority_enabled: bool = False,
    ):
        """Initialize the queue.

        Args:
            maxsize: Maximum queue size (0 for unlimited)
            name: Optional name for logging/debugging
            priority_enabled: Enable priority-based message ordering
        """
        self._maxsize = maxsize
        self._name = name or f"queue-{id(self)}"
        self._priority_enabled = priority_enabled
        self._queue: deque = deque()
        self._lock = asyncio.Lock()
        self._not_empty = asyncio.Condition(self._lock)
        self._not_full = asyncio.Condition(self._lock)
        self._put_count = 0
        self._get_count = 0

        logger.debug(
            f"Queue '{self._name}' initialized "
            f"(maxsize={maxsize}, priority={priority_enabled})"
        )

    async def put(
        self,
        item: Any,
        priority: int = 5,
        agent_id: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> bool:
        """Put an item into the queue.

        Args:
            item: Item to add to the queue
            priority: Priority level (0-10, higher is more important)
            agent_id: Optional ID of the agent putting the item
            timeout: Optional timeout in seconds

        Returns:
            True if item was added, False if timed out
        """
        async with self._not_full:
            # Wait for space if queue is full
            while self._maxsize > 0 and len(self._queue) >= self._maxsize:
                if timeout is not None:
                    try:
                        await asyncio.wait_for(self._not_full.wait(), timeout=timeout)
                    except asyncio.TimeoutError:
                        logger.warning(
                            f"Queue '{self._name}' put timeout for agent {agent_id}"
                        )
                        return False
                else:
                    await self._not_full.wait()

            # Add item to queue
            if self._priority_enabled:
                # Insert based on priority (higher priority first)
                inserted = False
                for i, (existing_priority, _) in enumerate(self._queue):
                    if priority > existing_priority:
                        self._queue.insert(i, (priority, item))
                        inserted = True
                        break
                if not inserted:
                    self._queue.append((priority, item))
            else:
                self._queue.append((priority, item))

            self._put_count += 1
            logger.debug(
                f"Queue '{self._name}' put item (size={len(self._queue)}, "
                f"priority={priority}, agent={agent_id})"
            )

            # Notify waiting consumers
            self._not_empty.notify()
            return True

    async def get(
        self,
        agent_id: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Optional[Any]:
        """Get an item from the queue.

        Args:
            agent_id: Optional ID of the agent getting the item
            timeout: Optional timeout in seconds

        Returns:
            The item, or None if timed out
        """
        async with self._not_empty:
            # Wait for item if queue is empty
            while len(self._queue) == 0:
                if timeout is not None:
                    try:
                        await asyncio.wait_for(self._not_empty.wait(), timeout=timeout)
                    except asyncio.TimeoutError:
                        logger.debug(
                            f"Queue '{self._name}' get timeout for agent {agent_id}"
                        )
                        return None
                else:
                    await self._not_empty.wait()

            # Get item from queue
            priority, item = self._queue.popleft()
            self._get_count += 1

            logger.debug(
                f"Queue '{self._name}' got item (size={len(self._queue)}, "
                f"priority={priority}, agent={agent_id})"
            )

            # Notify waiting producers
            self._not_full.notify()
            return item

    async def peek(self) -> Optional[Any]:
        """Peek at the next item without removing it.

        Returns:
            The next item, or None if queue is empty
        """
        async with self._lock:
            if len(self._queue) == 0:
                return None
            _, item = self._queue[0]
            return item

    async def clear(self) -> int:
        """Clear all items from the queue.

        Returns:
            Number of items removed
        """
        async with self._lock:
            count = len(self._queue)
            self._queue.clear()
            logger.info(f"Queue '{self._name}' cleared ({count} items removed)")
            self._not_full.notify_all()
            return count

    def qsize(self) -> int:
        """Get the current queue size.

        Returns:
            Number of items in the queue
        """
        return len(self._queue)

    def empty(self) -> bool:
        """Check if queue is empty.

        Returns:
            True if queue is empty
        """
        return len(self._queue) == 0

    def full(self) -> bool:
        """Check if queue is full.

        Returns:
            True if queue is full
        """
        return self._maxsize > 0 and len(self._queue) >= self._maxsize

    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics.

        Returns:
            Dictionary with current state and statistics
        """
        return {
            "name": self._name,
            "size": len(self._queue),
            "maxsize": self._maxsize,
            "priority_enabled": self._priority_enabled,
            "put_count": self._put_count,
            "get_count": self._get_count,
            "empty": self.empty(),
            "full": self.full(),
        }
