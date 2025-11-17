"""Integration tests for all reliability patterns.

Quick validation that all patterns work correctly together.
"""

import asyncio
import time
from src.reliability import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    retry,
    RetryError,
    timeout,
    TimeoutError,
    Bulkhead,
    BulkheadError,
)


async def test_circuit_breaker():
    """Test circuit breaker pattern."""
    print("\n[TEST] Circuit Breaker")

    cb = CircuitBreaker(failure_threshold=2, timeout=1.0)

    # Test is_open() - should be closed initially
    assert not cb.is_open(), "Circuit should start closed"
    assert cb.state == CircuitState.CLOSED, "State should be CLOSED"
    print("  ✓ Circuit starts in CLOSED state")

    # Test record_failure() - trigger opening
    await cb.record_failure()
    await cb.record_failure()
    assert cb.state == CircuitState.OPEN, "Circuit should be OPEN after failures"
    print("  ✓ Circuit opens after failure threshold")

    # Test is_open()
    assert cb.is_open(), "is_open() should return True"
    print("  ✓ is_open() works correctly")

    # Test call() when open - should raise error
    try:
        await cb.call(lambda: "test")
        assert False, "Should raise CircuitBreakerError"
    except CircuitBreakerError:
        print("  ✓ call() raises CircuitBreakerError when open")

    # Wait for timeout and test half-open
    await asyncio.sleep(1.1)
    cb._update_state()
    assert cb.state == CircuitState.HALF_OPEN, "Should transition to HALF_OPEN"
    print("  ✓ Circuit transitions to HALF_OPEN after timeout")

    # Test record_success()
    await cb.record_success()
    await cb.record_success()
    assert cb.state == CircuitState.CLOSED, "Should close after successes"
    print("  ✓ record_success() closes circuit from HALF_OPEN")

    print("  ✅ All circuit breaker tests passed")


async def test_retry():
    """Test retry pattern."""
    print("\n[TEST] Retry Decorator")

    attempt_count = 0

    @retry(max_attempts=3, exponential_base=1.5, exceptions=(ValueError,))
    async def flaky_function():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise ValueError("Temporary error")
        return "success"

    # Test retry with max_attempts
    result = await flaky_function()
    assert result == "success", "Should return success after retry"
    assert attempt_count == 2, "Should attempt twice"
    print("  ✓ @retry decorator with max_attempts works")

    # Test retry exhaustion
    attempt_count = 0

    @retry(max_attempts=2, exponential_base=1.5)
    async def always_fails():
        nonlocal attempt_count
        attempt_count += 1
        raise ValueError("Always fails")

    try:
        await always_fails()
        assert False, "Should raise RetryError"
    except RetryError as e:
        assert attempt_count == 2, "Should attempt max_attempts times"
        assert isinstance(e.last_exception, ValueError)
        print("  ✓ @retry raises RetryError after exhausting attempts")

    # Test exceptions tuple
    @retry(max_attempts=2, exceptions=(ValueError, KeyError))
    async def specific_exceptions():
        raise ValueError("Retryable")

    try:
        await specific_exceptions()
    except RetryError:
        print("  ✓ exceptions tuple parameter works")

    print("  ✅ All retry tests passed")


async def test_timeout():
    """Test timeout pattern."""
    print("\n[TEST] Timeout Decorator")

    # Test timeout enforcement
    @timeout(0.5)
    async def slow_function():
        await asyncio.sleep(1.0)
        return "done"

    try:
        await slow_function()
        assert False, "Should raise TimeoutError"
    except TimeoutError:
        print("  ✓ @timeout decorator enforces timeout")

    # Test success within timeout
    @timeout(1.0)
    async def fast_function():
        await asyncio.sleep(0.1)
        return "done"

    result = await fast_function()
    assert result == "done", "Should complete successfully"
    print("  ✓ @timeout allows completion within timeout")

    # Test asyncio.wait_for usage
    from src.reliability import wait_for

    async def test_func():
        await asyncio.sleep(0.1)
        return "result"

    result = await wait_for(test_func, 1.0)
    assert result == "result"
    print("  ✓ wait_for() helper function works")

    print("  ✅ All timeout tests passed")


async def test_bulkhead():
    """Test bulkhead pattern."""
    print("\n[TEST] Bulkhead")

    bulkhead = Bulkhead(max_workers=3, queue_size=5)

    # Test get_pool()
    pool = bulkhead.get_pool()
    assert pool is not None, "get_pool() should return executor"
    print("  ✓ get_pool() returns ThreadPoolExecutor")

    # Test execute() with sync function
    def sync_task(x):
        time.sleep(0.1)
        return x * 2

    result = await bulkhead.execute(sync_task, 5)
    assert result == 10, "Should execute sync function"
    print("  ✓ execute() works with sync functions")

    # Test execute() with async function
    async def async_task(x):
        await asyncio.sleep(0.1)
        return x * 3

    result = await bulkhead.execute(async_task, 5)
    assert result == 15, "Should execute async function"
    print("  ✓ execute() works with async functions")

    # Test max_workers isolation
    # Create a bulkhead without queue size limit for this test
    test_bulkhead = Bulkhead(max_workers=3)
    start = time.time()
    tasks = [test_bulkhead.execute(sync_task, i) for i in range(6)]
    await asyncio.gather(*tasks)
    duration = time.time() - start

    # With 3 workers and 6 tasks of 0.1s each, should take ~0.2s (2 batches)
    assert duration >= 0.2, "Should respect max_workers"
    print("  ✓ max_workers isolation works")
    await test_bulkhead.shutdown()

    # Test statistics
    stats = bulkhead.get_stats()
    assert stats["max_workers"] == 3
    assert stats["total_executions"] == 2  # sync + async task
    print("  ✓ Statistics tracking works")

    await bulkhead.shutdown()
    print("  ✅ All bulkhead tests passed")


async def test_combined_patterns():
    """Test combining multiple patterns."""
    print("\n[TEST] Combined Patterns")

    cb = CircuitBreaker(failure_threshold=3)
    bulkhead = Bulkhead(max_workers=5)

    @retry(max_attempts=2, exponential_base=1.5)
    @timeout(1.0)
    async def resilient_operation():
        if cb.is_open():
            raise CircuitBreakerError("Circuit open")

        async def operation():
            await asyncio.sleep(0.1)
            await cb.record_success()
            return "success"

        return await bulkhead.execute(operation)

    result = await resilient_operation()
    assert result == "success", "Combined patterns should work"
    print("  ✓ Circuit breaker + retry + timeout + bulkhead work together")

    await bulkhead.shutdown()
    print("  ✅ Combined patterns test passed")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("RELIABILITY PATTERNS INTEGRATION TESTS")
    print("=" * 60)

    try:
        await test_circuit_breaker()
        await test_retry()
        await test_timeout()
        await test_bulkhead()
        await test_combined_patterns()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
