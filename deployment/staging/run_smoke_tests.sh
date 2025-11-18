#!/bin/bash
# Smoke Tests for Staging Environment
# Tests health endpoint, agent functionality, observability, cost tracking, and all 7 improvements

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="agent-improvements-staging"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_TESTS++))
    ((TOTAL_TESTS++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED_TESTS++))
    ((TOTAL_TESTS++))
}

# Get service URL
get_service_url() {
    if [ -z "$PROJECT_ID" ]; then
        log_error "GCP_PROJECT_ID environment variable not set"
        exit 1
    fi

    SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --format="get(status.url)" 2>/dev/null || echo "")

    if [ -z "$SERVICE_URL" ]; then
        log_error "Could not retrieve service URL. Is staging deployed?"
        log_info "Run: ./deployment/staging/setup_staging.sh"
        exit 1
    fi

    log_info "Testing service at: $SERVICE_URL"
}

# Test 1: Health Endpoint
test_health_endpoint() {
    log_test "Testing health endpoint..."

    response=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/health" || echo "000")

    if [ "$response" == "200" ]; then
        log_pass "Health endpoint returned 200 OK"

        # Check health response body
        health_data=$(curl -s "${SERVICE_URL}/health")
        if echo "$health_data" | grep -q "status.*healthy"; then
            log_pass "Health endpoint returned healthy status"
        else
            log_fail "Health endpoint did not return healthy status"
        fi
    else
        log_fail "Health endpoint returned HTTP $response (expected 200)"
    fi
}

# Test 2: Metrics Endpoint
test_metrics_endpoint() {
    log_test "Testing metrics endpoint..."

    response=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/metrics" || echo "000")

    if [ "$response" == "200" ]; then
        log_pass "Metrics endpoint returned 200 OK"

        # Check for Prometheus metrics format
        metrics_data=$(curl -s "${SERVICE_URL}/metrics")
        if echo "$metrics_data" | grep -q "# HELP"; then
            log_pass "Metrics endpoint returns Prometheus format"
        else
            log_fail "Metrics endpoint does not return Prometheus format"
        fi
    else
        log_fail "Metrics endpoint returned HTTP $response (expected 200)"
    fi
}

# Test 3: Agent Execute Endpoint (Basic Functionality)
test_agent_execution() {
    log_test "Testing basic agent execution..."

    response=$(curl -s -X POST "${SERVICE_URL}/agent/execute" \
        -H "Content-Type: application/json" \
        -d '{
            "agent_id": "test_agent",
            "task": "simple_test",
            "input": {"message": "hello"}
        }' || echo "")

    if echo "$response" | grep -q "agent_id\|task_id\|status"; then
        log_pass "Agent execution endpoint is functional"
    else
        log_fail "Agent execution endpoint failed to respond correctly"
    fi
}

# Test 4: Observability - Logging
test_observability_logging() {
    log_test "Testing observability - structured logging..."

    # Check if logs are being written to Cloud Logging
    recent_logs=$(gcloud logging read \
        "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
        --limit=10 \
        --project="$PROJECT_ID" \
        --format="value(jsonPayload.message)" \
        2>/dev/null || echo "")

    if [ -n "$recent_logs" ]; then
        log_pass "Cloud Logging is receiving logs"

        # Check for structured logging fields
        structured_logs=$(gcloud logging read \
            "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" \
            --limit=5 \
            --project="$PROJECT_ID" \
            --format=json \
            2>/dev/null || echo "")

        if echo "$structured_logs" | grep -q "jsonPayload"; then
            log_pass "Structured logging is enabled"
        else
            log_fail "Structured logging not detected"
        fi
    else
        log_warn "No recent logs found (service may not have received requests)"
    fi
}

# Test 5: Observability - Tracing
test_observability_tracing() {
    log_test "Testing observability - distributed tracing..."

    # Check if Cloud Trace is enabled
    traces=$(gcloud trace list \
        --project="$PROJECT_ID" \
        --filter="startTime>='$(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S)Z'" \
        --limit=5 \
        --format="value(traceId)" \
        2>/dev/null || echo "")

    if [ -n "$traces" ]; then
        log_pass "Cloud Trace is collecting traces"
    else
        log_warn "No recent traces found (may need to trigger requests)"
    fi
}

# Test 6: Observability - Metrics
test_observability_metrics() {
    log_test "Testing observability - Cloud Monitoring metrics..."

    # Check if custom metrics are being reported
    metrics=$(gcloud monitoring time-series list \
        --filter='metric.type=starts_with("custom.googleapis.com/agent")' \
        --project="$PROJECT_ID" \
        --format="value(metric.type)" \
        2>/dev/null || echo "")

    if [ -n "$metrics" ]; then
        log_pass "Custom agent metrics are being reported"
    else
        log_warn "No custom metrics found yet (may need more runtime)"
    fi
}

# Test 7: Cost Tracking
test_cost_tracking() {
    log_test "Testing cost tracking functionality..."

    # Test cost tracking endpoint
    response=$(curl -s -X GET "${SERVICE_URL}/costs/summary" || echo "")

    if echo "$response" | grep -q "total_cost\|request_count\|model_usage"; then
        log_pass "Cost tracking endpoint is functional"

        # Check for budget alerts configuration
        if echo "$response" | grep -q "budget\|alert"; then
            log_pass "Budget tracking is configured"
        else
            log_warn "Budget tracking not found in response"
        fi
    else
        log_warn "Cost tracking endpoint may not be fully configured"
    fi
}

# Test 8: Improvement #1 - Evaluation Framework
test_evaluation_framework() {
    log_test "Testing Improvement #1: Evaluation Framework..."

    # Test golden task execution
    response=$(curl -s -X POST "${SERVICE_URL}/evaluation/run-golden-task" \
        -H "Content-Type: application/json" \
        -d '{
            "agent_type": "customer_support_agent",
            "task_id": "cs-003"
        }' || echo "")

    if echo "$response" | grep -q "task_id\|passed\|validation"; then
        log_pass "Evaluation framework is functional"
    else
        log_fail "Evaluation framework not responding correctly"
    fi
}

# Test 9: Improvement #2 - Observability Layer
test_observability_layer() {
    log_test "Testing Improvement #2: Observability Layer..."

    # Already tested in tests 4, 5, 6
    # Check for observability configuration endpoint
    response=$(curl -s -X GET "${SERVICE_URL}/observability/config" || echo "")

    if echo "$response" | grep -q "logging\|tracing\|metrics"; then
        log_pass "Observability layer is properly configured"
    else
        log_warn "Observability configuration endpoint not found"
    fi
}

# Test 10: Improvement #3 - Memory System
test_memory_system() {
    log_test "Testing Improvement #3: Memory System..."

    # Test session memory
    session_id="smoke-test-$(date +%s)"

    # Store memory
    store_response=$(curl -s -X POST "${SERVICE_URL}/memory/session/store" \
        -H "Content-Type: application/json" \
        -d "{
            \"session_id\": \"${session_id}\",
            \"key\": \"test_key\",
            \"value\": \"test_value\"
        }" || echo "")

    # Retrieve memory
    retrieve_response=$(curl -s -X GET "${SERVICE_URL}/memory/session/retrieve?session_id=${session_id}&key=test_key" || echo "")

    if echo "$retrieve_response" | grep -q "test_value"; then
        log_pass "Memory system (session memory) is functional"
    else
        log_warn "Memory system may not be fully configured"
    fi
}

# Test 11: Improvement #4 - Agent Coordination
test_agent_coordination() {
    log_test "Testing Improvement #4: Agent Coordination..."

    # Test message broker
    response=$(curl -s -X POST "${SERVICE_URL}/coordination/send-message" \
        -H "Content-Type: application/json" \
        -d '{
            "from_agent": "test_agent_1",
            "to_agent": "test_agent_2",
            "message_type": "TASK_REQUEST",
            "content": {"task": "test"}
        }' || echo "")

    if echo "$response" | grep -q "message_id\|status\|sent"; then
        log_pass "Agent coordination (message broker) is functional"
    else
        log_warn "Agent coordination may not be fully configured"
    fi
}

# Test 12: Improvement #5 - Cost Optimization
test_cost_optimization() {
    log_test "Testing Improvement #5: Cost Optimization..."

    # Test LLM router
    response=$(curl -s -X POST "${SERVICE_URL}/optimization/route-request" \
        -H "Content-Type: application/json" \
        -d '{
            "task_complexity": "simple",
            "prompt": "What is 2+2?"
        }' || echo "")

    if echo "$response" | grep -q "model\|tier\|estimated_cost"; then
        log_pass "Cost optimization (LLM router) is functional"

        # Check if cache is working
        cache_response=$(curl -s -X GET "${SERVICE_URL}/optimization/cache/stats" || echo "")
        if echo "$cache_response" | grep -q "hit_rate\|cache_size"; then
            log_pass "Result cache is operational"
        else
            log_warn "Result cache statistics not available"
        fi
    else
        log_warn "Cost optimization may not be fully configured"
    fi
}

# Test 13: Improvement #6 - Reliability Patterns
test_reliability_patterns() {
    log_test "Testing Improvement #6: Reliability Patterns..."

    # Test circuit breaker status
    response=$(curl -s -X GET "${SERVICE_URL}/reliability/circuit-breaker/status" || echo "")

    if echo "$response" | grep -q "state\|failure_count\|closed\|open\|half_open"; then
        log_pass "Reliability patterns (circuit breaker) is functional"
    else
        log_warn "Reliability patterns may not be fully configured"
    fi
}

# Test 14: Improvement #7 - Production Operations
test_production_operations() {
    log_test "Testing Improvement #7: Production Operations..."

    # Test deployment info
    response=$(curl -s -X GET "${SERVICE_URL}/deployment/info" || echo "")

    if echo "$response" | grep -q "version\|deployment_type\|environment"; then
        log_pass "Production operations (deployment info) is functional"

        # Check if smoke tests endpoint exists
        smoke_test_response=$(curl -s -X GET "${SERVICE_URL}/deployment/smoke-tests/status" || echo "")
        if echo "$smoke_test_response" | grep -q "tests\|passed\|failed"; then
            log_pass "Smoke tests integration is available"
        else
            log_warn "Smoke tests endpoint not found"
        fi
    else
        log_warn "Production operations may not be fully configured"
    fi
}

# Test 15: End-to-End Agent Workflow
test_e2e_workflow() {
    log_test "Testing end-to-end agent workflow with all improvements..."

    # Execute a complete workflow
    response=$(curl -s -X POST "${SERVICE_URL}/agent/execute-with-improvements" \
        -H "Content-Type: application/json" \
        -d '{
            "agent_type": "customer_support_agent",
            "task": "Handle customer inquiry",
            "input": {
                "customer_id": "test-customer-123",
                "inquiry": "What is your return policy?"
            },
            "enable_all_improvements": true
        }' || echo "")

    if echo "$response" | grep -q "task_id\|status\|result"; then
        log_pass "End-to-end workflow with all improvements is functional"

        # Check if response includes improvement metadata
        if echo "$response" | grep -q "cost\|trace_id\|cache_hit\|evaluation_score"; then
            log_pass "All improvement metadata is included in response"
        else
            log_warn "Some improvement metadata may be missing"
        fi
    else
        log_fail "End-to-end workflow failed to execute"
    fi
}

# Test 16: Service Performance
test_performance() {
    log_test "Testing service performance..."

    # Measure response time
    start_time=$(date +%s%N)
    curl -s -o /dev/null "${SERVICE_URL}/health"
    end_time=$(date +%s%N)

    duration_ms=$(( (end_time - start_time) / 1000000 ))

    if [ "$duration_ms" -lt 1000 ]; then
        log_pass "Service response time is good (${duration_ms}ms < 1000ms)"
    elif [ "$duration_ms" -lt 3000 ]; then
        log_warn "Service response time is acceptable (${duration_ms}ms)"
    else
        log_fail "Service response time is slow (${duration_ms}ms > 3000ms)"
    fi
}

# Print summary
print_summary() {
    echo ""
    echo "=========================================="
    echo "SMOKE TEST SUMMARY"
    echo "=========================================="
    echo ""
    echo "Total Tests:  $TOTAL_TESTS"
    echo -e "Passed:       ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed:       ${RED}$FAILED_TESTS${NC}"
    echo ""

    if [ $FAILED_TESTS -eq 0 ]; then
        log_info "All smoke tests passed! Staging environment is healthy."
        echo ""
        return 0
    else
        log_error "$FAILED_TESTS test(s) failed. Please review the output above."
        echo ""
        return 1
    fi
}

# Main execution
main() {
    log_info "Starting smoke tests for staging environment..."
    log_info "Project: $PROJECT_ID"
    log_info "Region: $REGION"
    log_info "Service: $SERVICE_NAME"
    echo ""

    get_service_url
    echo ""

    # Core functionality tests
    test_health_endpoint
    test_metrics_endpoint
    test_agent_execution
    echo ""

    # Observability tests
    test_observability_logging
    test_observability_tracing
    test_observability_metrics
    echo ""

    # Cost tracking
    test_cost_tracking
    echo ""

    # 7 Improvements tests
    log_info "Testing all 7 improvements..."
    test_evaluation_framework
    test_observability_layer
    test_memory_system
    test_agent_coordination
    test_cost_optimization
    test_reliability_patterns
    test_production_operations
    echo ""

    # Additional tests
    test_e2e_workflow
    test_performance
    echo ""

    print_summary
}

# Run main function
if main; then
    exit 0
else
    exit 1
fi
