"""Test script for Cost Optimization components."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from optimization.llm_router import LLMRouter, ComplexityLevel
from optimization.local_slm import LocalSLM
from optimization.caching import ResultCache
from optimization.cost_tracker import CostTracker, CostCategory


def test_llm_router():
    """Test LLM Router functionality."""
    print("\n=== Testing LLM Router ===")
    router = LLMRouter()

    # Test simple request
    simple_prompt = "Hello, how are you?"
    complexity = router.estimate_complexity(simple_prompt)
    model = router.route(simple_prompt)
    print(f"Simple prompt complexity: {complexity}")
    print(f"Routed to model: {model.model_name} (${model.cost_per_1k_tokens}/1K tokens)")

    # Test complex request
    complex_prompt = "Analyze the distributed architecture and design an optimization strategy for handling 10M concurrent users with sub-100ms latency requirements."
    complexity = router.estimate_complexity(complex_prompt, requires_reasoning=True)
    model = router.route(complex_prompt, requires_reasoning=True)
    print(f"\nComplex prompt complexity: {complexity}")
    print(f"Routed to model: {model.model_name} (${model.cost_per_1k_tokens}/1K tokens)")

    # Test cost estimation
    estimated_cost = router.estimate_cost(complex_prompt, expected_response_tokens=1000)
    print(f"Estimated cost: ${estimated_cost:.4f}")


def test_local_slm():
    """Test Local SLM functionality."""
    print("\n=== Testing Local SLM ===")
    slm = LocalSLM()

    # Test routine task detection
    prompts = [
        "Hello there!",
        "Calculate 25 + 37",
        "Extract emails from: contact@example.com and support@test.org",
        "Analyze the computational complexity of this distributed consensus algorithm"
    ]

    for prompt in prompts:
        is_routine, confidence, task_type = slm.is_routine_task(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Routine: {is_routine}, Confidence: {confidence:.2f}, Type: {task_type}")

        if is_routine:
            response = slm.execute(prompt)
            print(f"Local response: {response.content}")
            print(f"Execution time: {response.execution_time_ms:.2f}ms")

    print(f"\nLocal SLM Stats: {slm.get_stats()}")


def test_result_cache():
    """Test Result Cache functionality."""
    print("\n=== Testing Result Cache ===")
    cache = ResultCache(max_size=100, default_ttl_seconds=3600)

    # Test caching
    prompt = "What is machine learning?"
    key = cache.generate_key(prompt, model="gpt-4")
    print(f"Generated cache key: {key[:16]}...")

    # Set cache entry
    result = {"response": "Machine learning is a subset of artificial intelligence..."}
    cache.set(key, result, metadata={"model": "gpt-4", "prompt": prompt}, tags=["ml", "definition"])
    print("Stored result in cache")

    # Get from cache
    cached_result = cache.get(key)
    print(f"Retrieved from cache: {cached_result is not None}")

    # Test similar prompts
    similar_prompt = "what is machine learning"
    similar_key = cache.generate_key(similar_prompt, model="gpt-4")
    print(f"\nSimilar prompts generate similar keys: {key == similar_key}")

    # Get stats
    stats = cache.get_stats()
    print(f"\nCache Stats:")
    print(f"  Total requests: {stats.total_requests}")
    print(f"  Cache hits: {stats.cache_hits}")
    print(f"  Hit rate: {stats.hit_rate}%")
    print(f"  Total entries: {stats.total_entries}")


def test_cost_tracker():
    """Test Cost Tracker functionality."""
    print("\n=== Testing Cost Tracker ===")
    tracker = CostTracker()

    # Record some LLM calls
    tracker.record_llm_call(
        model_name="gpt-4",
        input_tokens=1000,
        output_tokens=500,
        agent_id="agent-001",
        user_id="user-001",
        task_id="task-001"
    )

    tracker.record_llm_call(
        model_name="gpt-3.5-turbo",
        input_tokens=500,
        output_tokens=300,
        agent_id="agent-001",
        user_id="user-001",
        task_id="task-002"
    )

    tracker.record_llm_call(
        model_name="local-slm",
        input_tokens=200,
        output_tokens=100,
        agent_id="agent-002",
        user_id="user-002",
        task_id="task-003"
    )

    # Get overall stats
    stats = tracker.get_stats()
    print(f"Total cost: ${stats.total_cost:.4f}")
    print(f"Total tokens: {stats.total_tokens}")
    print(f"Request count: {stats.request_count}")
    print(f"Average cost per request: ${stats.average_cost_per_request:.4f}")

    # Get agent stats
    agent_stats = tracker.get_agent_stats("agent-001")
    print(f"\nAgent-001 Stats:")
    print(f"  Total cost: ${agent_stats.total_cost:.4f}")
    print(f"  Request count: {agent_stats.request_count}")
    print(f"  Cost by model: {agent_stats.cost_by_model}")

    # Set budget and check status
    tracker.set_budget(limit=1.0, dimension="agent", identifier="agent-001")
    budget_status = tracker.get_budget_status(dimension="agent", identifier="agent-001")
    print(f"\nBudget Status for agent-001:")
    print(f"  Budget limit: ${budget_status['budget_limit']:.4f}")
    print(f"  Current spending: ${budget_status['current_spending']:.4f}")
    print(f"  Remaining: ${budget_status['remaining']:.4f}")
    print(f"  Percentage used: {budget_status['percentage_used']:.2f}%")

    # Get top spenders
    top_spenders = tracker.get_top_spenders(dimension="agent", limit=5)
    print(f"\nTop spending agents:")
    for agent_id, cost in top_spenders:
        print(f"  {agent_id}: ${cost:.4f}")


def test_integration():
    """Test integration of all components."""
    print("\n=== Testing Integration ===")

    # Initialize all components
    router = LLMRouter()
    slm = LocalSLM()
    cache = ResultCache()
    tracker = CostTracker()

    prompt = "Hello, how are you?"

    # 1. Check if local SLM can handle it
    is_routine, confidence, task_type = slm.is_routine_task(prompt)
    print(f"Is routine task: {is_routine} (confidence: {confidence:.2f})")

    if is_routine:
        # Handle locally - no cost!
        response = slm.execute(prompt)
        print(f"Handled locally: {response.content}")
        tracker.record(0.0, category=CostCategory.LLM_API, agent_id="agent-001")
    else:
        # 2. Check cache
        cache_key = cache.generate_key(prompt, model="gpt-4")
        cached_result = cache.get(cache_key)

        if cached_result:
            print("Result found in cache - no API call needed!")
            tracker.record(0.0, category=CostCategory.LLM_API, agent_id="agent-001")
        else:
            # 3. Route to appropriate model
            model_config = router.route(prompt)
            print(f"Routing to: {model_config.model_name}")

            # 4. Simulate LLM call and track cost
            tracker.record_llm_call(
                model_name=model_config.model_name,
                input_tokens=10,
                output_tokens=20,
                agent_id="agent-001"
            )

            # 5. Cache the result
            mock_result = {"response": "I'm doing well, thank you!"}
            cache.set(cache_key, mock_result, metadata={"model": model_config.model_name})
            print("Result cached for future requests")

    # Show final stats
    print(f"\nFinal Stats:")
    print(f"  Cache hit rate: {cache.get_stats().hit_rate}%")
    print(f"  Total cost: ${tracker.get_stats().total_cost:.4f}")
    print(f"  Local handling rate: {slm.get_stats()['local_handling_rate']}%")


if __name__ == "__main__":
    print("=" * 60)
    print("Cost Optimization Framework - Test Suite")
    print("=" * 60)

    try:
        test_llm_router()
        test_local_slm()
        test_result_cache()
        test_cost_tracker()
        test_integration()

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
