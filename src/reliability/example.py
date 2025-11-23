"""Example usage of reliability patterns.

This module demonstrates how to use the reliability patterns
in real-world scenarios.
"""

import asyncio
import random
from typing import Any

from .circuit_breaker import CircuitBreaker, CircuitBreakerError
from .retry import retry, RetryError
from .timeout import timeout, TimeoutError
from .bulkhead import Bulkhead


# Example 1: Circuit Breaker Pattern
async def example_circuit_breaker() -> None:
    """Demonstrate circuit breaker preventing cascading failures."""
    print("\n=== Circuit Breaker Example ===")

    cb = CircuitBreaker(failure_threshold=3, timeout=5.0)

    async def unreliable_service() -> str:
        """Simulates an unreliable external service."""
        if random.random() < 0.7:  # 70% failure rate
            raise Exception("Service unavailable")
        return "Success"

    # Make multiple calls - circuit will open after failures
    for i in range(10):
        try:
            result = await cb.call(unreliable_service)
            print(f"Call {i+1}: {result} - Circuit state: {cb.state.value}")
        except CircuitBreakerError as e:
            print(f"Call {i+1}: Circuit is open - {e}")
        except Exception as e:
            print(f"Call {i+1}: Failed - {e} - Circuit state: {cb.state.value}")

        await asyncio.sleep(0.5)


# Example 2: Retry Pattern with Exponential Backoff
@retry(max_attempts=3, exponential_base=2.0, exceptions=(ValueError,))
async def example_retry_function() -> str:
    """Demonstrate retry with exponential backoff."""
    if random.random() < 0.6:  # 60% failure rate
        raise ValueError("Temporary failure")
    return "Success after retry"


async def example_retry() -> None:
    """Demonstrate retry pattern."""
    print("\n=== Retry Pattern Example ===")

    try:
        result = await example_retry_function()
        print(f"Result: {result}")
    except RetryError as e:
        print(f"Failed after all retries: {e}")


# Example 3: Timeout Pattern
@timeout(2.0)
async def example_timeout_function(duration: float) -> str:
    """Demonstrate timeout enforcement."""
    await asyncio.sleep(duration)
    return f"Completed in {duration}s"


async def example_timeout_pattern() -> None:
    """Demonstrate timeout pattern."""
    print("\n=== Timeout Pattern Example ===")

    # This should succeed
    try:
        result = await example_timeout_function(1.0)
        print(f"Fast operation: {result}")
    except TimeoutError as e:
        print(f"Timed out: {e}")

    # This should timeout
    try:
        result = await example_timeout_function(3.0)
        print(f"Slow operation: {result}")
    except TimeoutError as e:
        print(f"Timed out: {e}")


# Example 4: Bulkhead Pattern
async def example_bulkhead() -> None:
    """Demonstrate bulkhead for resource isolation."""
    print("\n=== Bulkhead Pattern Example ===")

    bulkhead = Bulkhead(max_workers=3, name="example-bulkhead")

    def cpu_intensive_task(task_id: int) -> str:
        """Simulates CPU-intensive work."""
        import time
        time.sleep(1)
        return f"Task {task_id} completed"

    # Execute multiple tasks concurrently (limited by bulkhead)
    tasks = [
        bulkhead.execute(cpu_intensive_task, i)
        for i in range(5)
    ]

    print(f"Starting {len(tasks)} tasks with max_workers=3")
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        print(f"Task {i+1}: {result}")

    print(f"\nBulkhead stats: {bulkhead.get_stats()}")
    await bulkhead.shutdown()


# Example 5: Combining Patterns
class ResilientAPIClient:
    """Example API client using multiple reliability patterns."""

    def __init__(self):
        """Initialize resilient API client."""
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            timeout=30.0,
        )
        self.bulkhead = Bulkhead(max_workers=10, name="api-client")

    @retry(max_attempts=3, exponential_base=2.0)
    @timeout(5.0)
    async def fetch_data(self, endpoint: str) -> dict[str, Any]:
        """Fetch data with retry, timeout, and circuit breaker.

        Args:
            endpoint: API endpoint to call

        Returns:
            Response data
        """
        # Check circuit breaker
        if self.circuit_breaker.is_open():
            raise CircuitBreakerError("Circuit is open")

        # Execute through bulkhead
        async def api_call() -> dict[str, Any]:
            # Simulate API call
            await asyncio.sleep(random.uniform(0.1, 0.5))

            if random.random() < 0.2:  # 20% failure rate
                await self.circuit_breaker.record_failure()
                raise Exception("API error")

            await self.circuit_breaker.record_success()
            return {"endpoint": endpoint, "data": "response"}

        return await self.bulkhead.execute(api_call)

    async def shutdown(self) -> None:
        """Cleanup resources."""
        await self.bulkhead.shutdown()


async def example_combined_patterns() -> None:
    """Demonstrate combining multiple patterns."""
    print("\n=== Combined Patterns Example ===")

    client = ResilientAPIClient()

    # Make multiple API calls
    for i in range(5):
        try:
            result = await client.fetch_data(f"/api/endpoint/{i}")
            print(f"Request {i+1}: Success - {result}")
        except (TimeoutError, RetryError, CircuitBreakerError) as e:
            print(f"Request {i+1}: Failed - {type(e).__name__}: {e}")
        except Exception as e:
            print(f"Request {i+1}: Error - {e}")

    await client.shutdown()


async def main() -> None:
    """Run all examples."""
    await example_circuit_breaker()
    await example_retry()
    await example_timeout_pattern()
    await example_bulkhead()
    await example_combined_patterns()


if __name__ == "__main__":
    asyncio.run(main())
