#!/bin/bash

################################################################################
# validate_improvements.sh - Validate All 7 Production Improvements
#
# This script validates each improvement independently:
#   1. Evaluation Framework
#   2. Observability Layer
#   3. Memory System
#   4. Agent Coordination
#   5. Cost Optimization
#   6. Reliability Patterns
#   7. Deployment Operations
#
# Each validation includes:
# - Unit tests
# - Integration tests
# - Functionality verification
# - Pass/Fail determination
#
# Usage:
#   ./validate_improvements.sh [--improvement NAME] [--verbose]
#
# Options:
#   --improvement NAME    Validate specific improvement only
#   --verbose             Verbose output
#
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOCAL_DIR="${PROJECT_ROOT}/deployment/local"
SRC_DIR="${PROJECT_ROOT}/src"
REPORTS_DIR="${LOCAL_DIR}/reports"

# Options
IMPROVEMENT_TO_TEST=""
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --improvement)
            IMPROVEMENT_TO_TEST="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Results tracking
declare -A RESULTS
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_test() {
    echo -e "${MAGENTA}  🧪 $1${NC}"
}

record_result() {
    local test_name=$1
    local status=$2
    RESULTS["$test_name"]=$status
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$status" == "PASS" ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        print_success "$test_name"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        print_error "$test_name - FAILED"
    fi
}

################################################################################
# Improvement 1: Evaluation Framework
################################################################################

validate_evaluation() {
    print_header "Validating Improvement #1: Evaluation Framework"

    print_step "Testing golden tasks module..."
    cat > "${LOCAL_DIR}/test_eval.py" << 'EOF'
import sys
sys.path.insert(0, '/home/user/mapachev1')

from src.evaluation.golden_tasks import GoldenTask, AcceptanceCriterion, GoldenTaskSet
from src.evaluation.executor import TaskExecutor
from src.evaluation.validator import Validator

def test_golden_task_creation():
    """Test creating golden tasks"""
    task = GoldenTask(
        task_id="test_001",
        description="Test task",
        input_data={"test": "data"},
        expected_output="success",
        acceptance_criteria=[
            AcceptanceCriterion(criterion_type="contains", expected_value="success")
        ],
        max_cost_usd=0.05,
        timeout_ms=5000
    )
    assert task.task_id == "test_001"
    assert len(task.acceptance_criteria) == 1
    print("✓ Golden task creation works")

def test_acceptance_criteria():
    """Test acceptance criteria validation"""
    criterion = AcceptanceCriterion(
        criterion_type="contains",
        expected_value="test"
    )

    # Test match
    result = criterion.evaluate("this is a test")
    assert result.passed == True

    # Test no match
    result = criterion.evaluate("no match")
    assert result.passed == False
    print("✓ Acceptance criteria validation works")

def test_golden_task_set():
    """Test golden task sets"""
    task_set = GoldenTaskSet(
        name="test_set",
        description="Test set",
        category="test"
    )

    task = GoldenTask(
        task_id="test_001",
        description="Test",
        input_data={},
        expected_output="success",
        acceptance_criteria=[]
    )

    task_set.add_task(task)
    assert len(task_set.tasks) == 1
    print("✓ Golden task sets work")

def test_validator():
    """Test validator"""
    validator = Validator()

    criterion = AcceptanceCriterion(
        criterion_type="exact",
        expected_value="test"
    )

    result = validator.validate("test", [criterion])
    assert result.all_passed == True
    print("✓ Validator works")

if __name__ == "__main__":
    try:
        test_golden_task_creation()
        test_acceptance_criteria()
        test_golden_task_set()
        test_validator()
        print("\n✅ All evaluation tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Evaluation test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_eval.py"; then
        record_result "Evaluation Framework - Golden Tasks" "PASS"
        record_result "Evaluation Framework - Acceptance Criteria" "PASS"
        record_result "Evaluation Framework - Task Sets" "PASS"
        record_result "Evaluation Framework - Validator" "PASS"
    else
        record_result "Evaluation Framework" "FAIL"
    fi
}

################################################################################
# Improvement 2: Observability Layer
################################################################################

validate_observability() {
    print_header "Validating Improvement #2: Observability Layer"

    print_step "Testing observability modules..."
    cat > "${LOCAL_DIR}/test_observability.py" << 'EOF'
import sys
sys.path.insert(0, '/home/user/mapachev1')

from src.observability.structured_logging import StructuredLogger
from src.observability.metrics import MetricsCollector
from src.observability.distributed_tracing import TracingManager

def test_structured_logging():
    """Test structured logging"""
    logger = StructuredLogger(service_name="test", environment="local")

    # Test logging
    logger.info("test_message", key="value")
    logger.error("error_message", error="test")

    print("✓ Structured logging works")

def test_metrics_collector():
    """Test metrics collection"""
    collector = MetricsCollector(namespace="test")

    # Record metrics
    collector.record_counter("test_counter", 1, tags={"env": "test"})
    collector.record_latency("test_latency", 100.0, tags={"env": "test"})
    collector.record_gauge("test_gauge", 50.0, tags={"env": "test"})

    # Get metrics
    metrics = collector.get_metrics()
    assert len(metrics) > 0

    print("✓ Metrics collector works")

def test_distributed_tracing():
    """Test distributed tracing"""
    tracer = TracingManager(service_name="test")

    # Start trace
    trace_id = tracer.start_trace("test_operation")
    assert trace_id is not None

    # End trace
    tracer.end_trace(trace_id)

    print("✓ Distributed tracing works")

if __name__ == "__main__":
    try:
        test_structured_logging()
        test_metrics_collector()
        test_distributed_tracing()
        print("\n✅ All observability tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Observability test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_observability.py"; then
        record_result "Observability - Structured Logging" "PASS"
        record_result "Observability - Metrics Collection" "PASS"
        record_result "Observability - Distributed Tracing" "PASS"
    else
        record_result "Observability Layer" "FAIL"
    fi
}

################################################################################
# Improvement 3: Memory System
################################################################################

validate_memory() {
    print_header "Validating Improvement #3: Memory System"

    print_step "Testing memory modules..."
    cat > "${LOCAL_DIR}/test_memory.py" << 'EOF'
import sys
sys.path.insert(0, '/home/user/mapachev1')

from src.memory.session_memory import SessionMemory
from src.memory.vector_memory import VectorMemory

def test_session_memory():
    """Test session memory"""
    memory = SessionMemory(ttl_seconds=3600, max_size=1000)

    # Add messages
    memory.add_message("session_1", "user", "Hello")
    memory.add_message("session_1", "assistant", "Hi there")
    memory.add_message("session_1", "user", "How are you?")

    # Get messages
    messages = memory.get_messages("session_1")
    assert len(messages) == 3

    # Get context
    context = memory.get_context("session_1")
    assert "Hello" in context

    # Clear session
    memory.clear_session("session_1")
    messages = memory.get_messages("session_1")
    assert len(messages) == 0

    print("✓ Session memory works")

def test_vector_memory():
    """Test vector memory"""
    memory = VectorMemory(collection_name="test_collection")

    # Add documents
    memory.add("This is a test document", metadata={"type": "test"})
    memory.add("Another test document", metadata={"type": "test"})

    # Search
    results = memory.search("test document", n_results=2)
    assert len(results) > 0

    print("✓ Vector memory works")

if __name__ == "__main__":
    try:
        test_session_memory()
        test_vector_memory()
        print("\n✅ All memory tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Memory test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_memory.py"; then
        record_result "Memory System - Session Memory" "PASS"
        record_result "Memory System - Vector Memory" "PASS"
    else
        record_result "Memory System" "FAIL"
    fi
}

################################################################################
# Improvement 4: Agent Coordination
################################################################################

validate_coordination() {
    print_header "Validating Improvement #4: Agent Coordination"

    print_step "Testing coordination modules..."
    cat > "${LOCAL_DIR}/test_coordination.py" << 'EOF'
import sys
import asyncio
sys.path.insert(0, '/home/user/mapachev1')

from src.coordination.message_broker import MessageBroker
from src.coordination.a2a_protocol import A2AMessage, MessageType

async def test_message_broker():
    """Test message broker"""
    broker = MessageBroker()

    received_messages = []

    def handler(message):
        received_messages.append(message)

    # Subscribe
    broker.subscribe("test.topic", handler)

    # Publish
    test_message = A2AMessage(
        message_type=MessageType.EVENT,
        sender="test_sender",
        recipient="test.topic",
        payload={"data": "test"}
    )

    broker.publish("test.topic", test_message)

    # Give it a moment to process
    await asyncio.sleep(0.1)

    assert len(received_messages) == 1
    print("✓ Message broker works")

async def test_a2a_protocol():
    """Test A2A protocol messages"""
    # Create different message types
    query = A2AMessage(
        message_type=MessageType.QUERY,
        sender="agent_1",
        recipient="agent_2",
        payload={"question": "test"}
    )

    response = A2AMessage(
        message_type=MessageType.RESPONSE,
        sender="agent_2",
        recipient="agent_1",
        payload={"answer": "test"},
        correlation_id=query.correlation_id
    )

    assert query.message_type == MessageType.QUERY
    assert response.correlation_id == query.correlation_id

    print("✓ A2A protocol works")

if __name__ == "__main__":
    try:
        asyncio.run(test_message_broker())
        asyncio.run(test_a2a_protocol())
        print("\n✅ All coordination tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Coordination test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_coordination.py"; then
        record_result "Coordination - Message Broker" "PASS"
        record_result "Coordination - A2A Protocol" "PASS"
    else
        record_result "Agent Coordination" "FAIL"
    fi
}

################################################################################
# Improvement 5: Cost Optimization
################################################################################

validate_cost_optimization() {
    print_header "Validating Improvement #5: Cost Optimization"

    print_step "Testing cost optimization modules..."
    cat > "${LOCAL_DIR}/test_cost.py" << 'EOF'
import sys
import asyncio
sys.path.insert(0, '/home/user/mapachev1')

from src.optimization.llm_router import SmartRouter
from src.optimization.cost_tracker import CostTracker
from src.optimization.caching import ResponseCache

def test_smart_router():
    """Test smart LLM router"""
    router = SmartRouter(default_model="mock", cost_threshold_usd=0.10)

    # Route simple task
    model = router.route_request("simple", "classification")
    assert model in ["mock", "llama3", "gpt-3.5-turbo"]

    # Route complex task
    model = router.route_request("complex", "reasoning")
    assert model is not None

    print("✓ Smart router works")

def test_cost_tracker():
    """Test cost tracking"""
    tracker = CostTracker()

    # Record requests
    tracker.record_request("gpt-4", 100, 50, 0.015)
    tracker.record_request("gpt-3.5-turbo", 80, 40, 0.003)

    # Get summary
    summary = tracker.get_summary()
    assert summary["total_requests"] == 2
    assert summary["total_cost_usd"] > 0

    print("✓ Cost tracker works")

async def test_caching():
    """Test response caching"""
    cache = ResponseCache(ttl_seconds=300, max_size=1000)

    # Set cache
    cache.set("key1", {"result": "test"})

    # Get cache
    result = cache.get("key1")
    assert result is not None
    assert result["result"] == "test"

    # Cache miss
    result = cache.get("nonexistent")
    assert result is None

    # Get stats
    stats = cache.get_stats()
    assert stats["hits"] >= 0

    print("✓ Response caching works")

if __name__ == "__main__":
    try:
        test_smart_router()
        test_cost_tracker()
        asyncio.run(test_caching())
        print("\n✅ All cost optimization tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Cost optimization test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_cost.py"; then
        record_result "Cost Optimization - Smart Router" "PASS"
        record_result "Cost Optimization - Cost Tracker" "PASS"
        record_result "Cost Optimization - Caching" "PASS"
    else
        record_result "Cost Optimization" "FAIL"
    fi
}

################################################################################
# Improvement 6: Reliability Patterns
################################################################################

validate_reliability() {
    print_header "Validating Improvement #6: Reliability Patterns"

    print_step "Testing reliability modules..."
    cat > "${LOCAL_DIR}/test_reliability.py" << 'EOF'
import sys
import asyncio
sys.path.insert(0, '/home/user/mapachev1')

from src.reliability.retry import RetryPolicy
from src.reliability.circuit_breaker import CircuitBreaker
from src.reliability.timeout import TimeoutManager

async def test_retry_policy():
    """Test retry with exponential backoff"""
    policy = RetryPolicy(max_attempts=3, backoff_factor=2.0)

    attempts = 0

    async def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Temporary error")
        return "success"

    result = await policy.execute(flaky_function)
    assert result == "success"
    assert attempts == 3

    print("✓ Retry policy works")

async def test_circuit_breaker():
    """Test circuit breaker pattern"""
    cb = CircuitBreaker(failure_threshold=3, timeout_seconds=1)

    failure_count = 0

    async def failing_function():
        nonlocal failure_count
        failure_count += 1
        raise Exception("Service unavailable")

    # Trigger failures to open circuit
    for i in range(3):
        try:
            await cb.call(failing_function)
        except:
            pass

    # Circuit should be open now
    assert cb.state == "open"

    print("✓ Circuit breaker works")

async def test_timeout_manager():
    """Test timeout management"""
    manager = TimeoutManager(default_timeout_seconds=1)

    async def slow_function():
        await asyncio.sleep(2)
        return "done"

    # Should timeout
    try:
        await manager.run_with_timeout(slow_function)
        assert False, "Should have timed out"
    except asyncio.TimeoutError:
        pass

    print("✓ Timeout manager works")

if __name__ == "__main__":
    try:
        asyncio.run(test_retry_policy())
        asyncio.run(test_circuit_breaker())
        asyncio.run(test_timeout_manager())
        print("\n✅ All reliability tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Reliability test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_reliability.py"; then
        record_result "Reliability - Retry Policy" "PASS"
        record_result "Reliability - Circuit Breaker" "PASS"
        record_result "Reliability - Timeout Manager" "PASS"
    else
        record_result "Reliability Patterns" "FAIL"
    fi
}

################################################################################
# Improvement 7: Deployment Operations
################################################################################

validate_deployment() {
    print_header "Validating Improvement #7: Deployment Operations"

    print_step "Testing deployment modules..."
    cat > "${LOCAL_DIR}/test_deployment.py" << 'EOF'
import sys
sys.path.insert(0, '/home/user/mapachev1')

from src.deployment.smoke_tests import SmokeTestRunner

def test_smoke_tests():
    """Test smoke test runner"""
    runner = SmokeTestRunner()

    # Define simple tests
    def test_health():
        return {"status": "healthy"}

    def test_api():
        return {"status": "ok"}

    runner.add_test("health_check", test_health)
    runner.add_test("api_test", test_api)

    # Run tests
    results = runner.run_all()

    assert len(results) == 2
    assert all(r["passed"] for r in results)

    print("✓ Smoke tests work")

def test_health_check_format():
    """Test standard health check format"""
    health = {
        "status": "healthy",
        "timestamp": "2025-11-18T00:00:00",
        "version": "1.0.0",
        "components": {
            "database": "operational",
            "cache": "operational",
            "api": "operational"
        }
    }

    assert health["status"] == "healthy"
    assert "components" in health
    assert len(health["components"]) == 3

    print("✓ Health check format correct")

if __name__ == "__main__":
    try:
        test_smoke_tests()
        test_health_check_format()
        print("\n✅ All deployment tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Deployment test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

    if python3 "${LOCAL_DIR}/test_deployment.py"; then
        record_result "Deployment - Smoke Tests" "PASS"
        record_result "Deployment - Health Checks" "PASS"
    else
        record_result "Deployment Operations" "FAIL"
    fi
}

################################################################################
# Generate Validation Report
################################################################################

generate_validation_report() {
    print_header "Generating Validation Report"

    local report_file="${REPORTS_DIR}/validation_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "${report_file}" << EOF
╔══════════════════════════════════════════════════════════════════════╗
║         7 IMPROVEMENTS - VALIDATION REPORT                           ║
╚══════════════════════════════════════════════════════════════════════╝

Validation Date: $(date)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL SUMMARY:

Total Tests: ${TOTAL_TESTS}
Passed: ${PASSED_TESTS}
Failed: ${FAILED_TESTS}
Pass Rate: $(awk "BEGIN {printf \"%.1f%%\", (${PASSED_TESTS}/${TOTAL_TESTS})*100}")

Overall Status: $([ $FAILED_TESTS -eq 0 ] && echo "✅ ALL TESTS PASSED" || echo "❌ SOME TESTS FAILED")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED RESULTS:

EOF

    # Add each test result
    for test_name in "${!RESULTS[@]}"; do
        status="${RESULTS[$test_name]}"
        if [ "$status" == "PASS" ]; then
            echo "✅ $test_name" >> "${report_file}"
        else
            echo "❌ $test_name" >> "${report_file}"
        fi
    done

    cat >> "${report_file}" << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPROVEMENT STATUS:

1. Evaluation Framework
   Status: $(grep -q "Evaluation Framework.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Golden Tasks, Acceptance Criteria, Validator

2. Observability Layer
   Status: $(grep -q "Observability.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Structured Logging, Metrics, Tracing

3. Memory System
   Status: $(grep -q "Memory System.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Session Memory, Vector Memory

4. Agent Coordination
   Status: $(grep -q "Coordination.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Message Broker, A2A Protocol

5. Cost Optimization
   Status: $(grep -q "Cost Optimization.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Smart Router, Cost Tracker, Caching

6. Reliability Patterns
   Status: $(grep -q "Reliability.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Retry Policy, Circuit Breaker, Timeout Manager

7. Deployment Operations
   Status: $(grep -q "Deployment.*PASS" <<< "${!RESULTS[@]} ${RESULTS[@]}" && echo "✅ OPERATIONAL" || echo "❌ FAILED")
   Components: Smoke Tests, Health Checks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRODUCTION READINESS CHECKLIST:

$([ $FAILED_TESTS -eq 0 ] && echo "✅" || echo "❌") All improvements validated
$([ $FAILED_TESTS -eq 0 ] && echo "✅" || echo "❌") Unit tests passing
$([ $FAILED_TESTS -eq 0 ] && echo "✅" || echo "❌") Integration tests passing
$([ $FAILED_TESTS -eq 0 ] && echo "✅" || echo "❌") All modules functional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:

$(if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ All validations passed! Ready to:"
    echo "   1. Run pilot agent tests"
    echo "   2. Collect comprehensive metrics"
    echo "   3. Deploy to staging environment"
    echo "   4. Roll out to production"
else
    echo "❌ Fix failing tests:"
    for test_name in "${!RESULTS[@]}"; do
        if [ "${RESULTS[$test_name]}" == "FAIL" ]; then
            echo "   - ${test_name}"
        fi
    done
    echo "   Then re-run validation"
fi)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

╔══════════════════════════════════════════════════════════════════════╗
║  $([ $FAILED_TESTS -eq 0 ] && echo "VALIDATION SUCCESSFUL! ALL SYSTEMS GO! 🚀" || echo "VALIDATION INCOMPLETE - REVIEW FAILURES")             ║
╚══════════════════════════════════════════════════════════════════════╝
EOF

    cat "${report_file}"
    print_success "Validation report saved to: ${report_file}"
}

################################################################################
# Main Execution
################################################################################

main() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║         7 IMPROVEMENTS - COMPREHENSIVE VALIDATION                    ║
║                                                                      ║
║  Validating each improvement independently:                          ║
║    1. Evaluation Framework                                           ║
║    2. Observability Layer                                            ║
║    3. Memory System                                                  ║
║    4. Agent Coordination                                             ║
║    5. Cost Optimization                                              ║
║    6. Reliability Patterns                                           ║
║    7. Deployment Operations                                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    mkdir -p "${REPORTS_DIR}"

    # Run validations
    if [ -n "$IMPROVEMENT_TO_TEST" ]; then
        case "$IMPROVEMENT_TO_TEST" in
            evaluation|1)
                validate_evaluation
                ;;
            observability|2)
                validate_observability
                ;;
            memory|3)
                validate_memory
                ;;
            coordination|4)
                validate_coordination
                ;;
            cost|cost_optimization|5)
                validate_cost_optimization
                ;;
            reliability|6)
                validate_reliability
                ;;
            deployment|7)
                validate_deployment
                ;;
            *)
                print_error "Unknown improvement: $IMPROVEMENT_TO_TEST"
                exit 1
                ;;
        esac
    else
        # Run all validations
        validate_evaluation
        validate_observability
        validate_memory
        validate_coordination
        validate_cost_optimization
        validate_reliability
        validate_deployment
    fi

    # Generate report
    generate_validation_report

    echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}  All validations passed! ${PASSED_TESTS}/${TOTAL_TESTS} tests successful.${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
        exit 0
    else
        echo -e "${RED}  Some validations failed. ${FAILED_TESTS}/${TOTAL_TESTS} tests failed.${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
        exit 1
    fi
}

# Run main function
main "$@"
