# Reliability Patterns

Production-ready implementations of reliability patterns for fault-tolerant systems.

## Overview

This module provides four essential reliability patterns:

1. **Circuit Breaker** - Prevents cascading failures
2. **Retry** - Handles transient failures with exponential backoff
3. **Timeout** - Prevents indefinite waits
4. **Bulkhead** - Isolates resources and prevents exhaustion

All patterns use type hints, async/await, and work without cloud resources.

## Circuit Breaker

Monitors failures and temporarily blocks calls when failure threshold is exceeded.

### States
- **CLOSED**: Normal operation, requests pass through
- **OPEN**: Too many failures, requests blocked
- **HALF_OPEN**: Testing recovery, limited calls allowed

### Usage

```python
from src.reliability import CircuitBreaker, CircuitBreakerError

cb = CircuitBreaker(
    failure_threshold=5,    # Open after 5 failures
    success_threshold=2,    # Close after 2 successes in half-open
    timeout=60.0,          # Seconds before half-open
)

# Check state
if cb.is_open():
    print("Circuit is open, service unavailable")

# Execute through circuit breaker
try:
    result = await cb.call(external_service_call)
except CircuitBreakerError:
    print("Circuit is open")

# Manual recording
await cb.record_success()
await cb.record_failure()
```

### Methods
- `is_open()` - Check if circuit is open
- `is_closed()` - Check if circuit is closed
- `is_half_open()` - Check if circuit is half-open
- `call(func, *args, **kwargs)` - Execute function through circuit breaker
- `record_success()` - Record successful call
- `record_failure()` - Record failed call
- `reset()` - Reset to initial state

## Retry

Decorator for retrying functions with exponential backoff.

### Usage

```python
from src.reliability import retry, RetryError

@retry(
    max_attempts=3,        # Try up to 3 times
    exponential_base=2.0,  # 2^0=1s, 2^1=2s, 2^2=4s
    max_delay=60.0,        # Cap at 60 seconds
    exceptions=(ValueError, ConnectionError),
    jitter=True,           # Add randomness to prevent thundering herd
)
async def fetch_data():
    response = await http_client.get("/api/data")
    return response.json()

try:
    data = await fetch_data()
except RetryError as e:
    print(f"Failed after all retries: {e.last_exception}")
```

### Context Manager

```python
from src.reliability import AsyncRetry

retry_policy = AsyncRetry(max_attempts=5, exponential_base=2.0)

async for attempt in retry_policy:
    async with attempt:
        result = await risky_operation()
        break  # Success
```

## Timeout

Decorator for enforcing timeouts on async operations.

### Usage

```python
from src.reliability import timeout, TimeoutError

@timeout(5.0)  # 5 second timeout
async def fetch_user(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            return await response.json()

try:
    user = await fetch_user(123)
except TimeoutError:
    print("Request timed out")
```

### Helper Function

```python
from src.reliability import wait_for

result = await wait_for(fetch_user, 5.0, user_id=123)
```

### Timeout Manager

```python
from src.reliability import TimeoutManager

manager = TimeoutManager()

tasks = [
    manager.run(fetch_user, 5.0, user_id=1),
    manager.run(fetch_orders, 10.0, user_id=1),
    manager.run(fetch_profile, 3.0, user_id=1),
]

results = await asyncio.gather(*tasks, return_exceptions=True)
```

## Bulkhead

Isolates resources using ThreadPoolExecutor to prevent exhaustion.

### Usage

```python
from src.reliability import Bulkhead, BulkheadError

bulkhead = Bulkhead(
    max_workers=10,      # Max concurrent workers
    queue_size=100,      # Max queue size
    name="database",     # Optional name
)

# Execute function in isolated pool
result = await bulkhead.execute(cpu_intensive_task, arg1, arg2)

# Check capacity
if bulkhead.available_capacity() > 0:
    result = await bulkhead.execute(another_task)

# Get statistics
stats = bulkhead.get_stats()
print(stats)  # name, max_workers, active_tasks, etc.

# Cleanup
await bulkhead.shutdown(wait=True)
```

### Context Manager

```python
async with Bulkhead(max_workers=5) as bulkhead:
    result = await bulkhead.execute(task)
# Automatically shuts down on exit
```

### Bulkhead Registry

```python
from src.reliability import BulkheadRegistry

registry = BulkheadRegistry()

# Create bulkheads for different resources
await registry.create("database", max_workers=5)
await registry.create("cache", max_workers=10)
await registry.create("api", max_workers=20)

# Use bulkheads
db = registry.get("database")
result = await db.execute(query_database, sql)

# Get all stats
all_stats = registry.get_all_stats()

# Cleanup
await registry.shutdown_all()
```

## Combining Patterns

These patterns work together to create highly resilient systems:

```python
from src.reliability import (
    CircuitBreaker,
    retry,
    timeout,
    Bulkhead,
)

class ResilientAPIClient:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=5)
        self.bulkhead = Bulkhead(max_workers=10)

    @retry(max_attempts=3)
    @timeout(5.0)
    async def fetch_data(self, endpoint: str):
        if self.circuit_breaker.is_open():
            raise CircuitBreakerError("Circuit is open")

        async def api_call():
            # Your API call logic
            result = await make_request(endpoint)
            await self.circuit_breaker.record_success()
            return result

        return await self.bulkhead.execute(api_call)
```

## Error Handling

Each pattern has its own exception type:

- `CircuitBreakerError` - Circuit breaker is open
- `RetryError` - All retry attempts exhausted
- `TimeoutError` - Operation exceeded timeout
- `BulkheadError` - Bulkhead capacity exceeded

## Best Practices

1. **Circuit Breaker**
   - Set failure_threshold based on acceptable error rate
   - Use timeout appropriate for service recovery time
   - Monitor state transitions

2. **Retry**
   - Only retry on transient failures (network errors, timeouts)
   - Don't retry on client errors (400, 401, 403, 404)
   - Use jitter to prevent thundering herd
   - Set reasonable max_delay to prevent long waits

3. **Timeout**
   - Set timeout based on SLA requirements
   - Consider network latency and processing time
   - Use timeout with retry for best results

4. **Bulkhead**
   - Size max_workers based on resource limits
   - Group operations by resource type
   - Monitor statistics regularly
   - Always shutdown to release resources

## Performance Considerations

- **Circuit Breaker**: Minimal overhead, uses asyncio.Lock
- **Retry**: Exponential backoff prevents overwhelming services
- **Timeout**: Uses asyncio.wait_for, no polling overhead
- **Bulkhead**: ThreadPoolExecutor for CPU-bound tasks, async for I/O-bound

## Testing

See `example.py` for comprehensive examples of all patterns.

```bash
python -m src.reliability.example
```

## Requirements

- Python 3.10+
- asyncio
- typing
- concurrent.futures (stdlib)

No external dependencies or cloud resources required.
