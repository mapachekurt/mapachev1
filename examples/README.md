# Agent Improvement Framework Examples

This directory contains comprehensive, executable examples that demonstrate the value of the 7 agent improvements framework.

## Examples

### 1. Before/After Agent Comparison (`before_after_agent.py`)

**Purpose**: Shows the dramatic difference between a basic agent and a production-ready agent with all 7 improvements integrated.

**What it demonstrates**:
- **BEFORE**: Basic agent with just LLM calls (no observability, reliability, or cost tracking)
- **AFTER**: Production agent with all 7 improvements:
  1. Observability (structured logging, metrics, tracing)
  2. Reliability (retry logic, circuit breakers, timeouts)
  3. Cost Optimization (cost tracking, caching, budget management)
  4. Memory Management (session memory, conversation history)
  5. Coordination (A2A messaging capability)
  6. Evaluation (quality scoring and validation)
  7. Deployment (health checks, graceful degradation)

**Run it**:
```bash
python examples/before_after_agent.py
```

**Expected output**:
- Side-by-side comparison of basic vs production agent
- Detailed metrics showing cost, performance, and quality
- Clear value proposition for each improvement

**Key metrics shown**:
- Cost per request: ~$0.0015
- Quality scores: 1.00
- Circuit breaker state: closed
- Budget tracking: real-time monitoring
- Session management: active sessions tracked

---

### 2. Multi-Agent Workflow (`multi_agent_workflow.py`)

**Purpose**: Demonstrates a realistic multi-agent system where 3-4 agents coordinate to complete a complex workflow.

**What it demonstrates**:
- **Agent Roles**:
  - Coordinator Agent: Orchestrates the workflow
  - Research Agent: Gathers and analyzes information
  - Writer Agent: Creates content based on research
  - Reviewer Agent: Validates quality and provides feedback

- **Patterns shown**:
  - A2A (Agent-to-Agent) communication protocol
  - Hierarchical coordination pattern
  - Async execution with proper error handling
  - Shared observability across all agents
  - Cost tracking across the entire workflow
  - Reliability patterns (retry, circuit breaker)
  - Quality gates and revision loops

**Run it**:
```bash
python examples/multi_agent_workflow.py
```

**Expected output**:
- Complete workflow execution from topic to final content
- Per-agent cost breakdown
- Quality assessment with automatic revision
- System-wide statistics and metrics

**Key metrics shown**:
- Total workflow cost: ~$0.010
- Quality score: 0.75-1.00
- Individual agent contributions
- Token usage per agent
- Budget status and alerts

---

## Use Case: Content Creation Pipeline

The multi-agent workflow demonstrates a real-world use case:

**Input**: Topic request (e.g., "Artificial Intelligence in Healthcare")

**Process**:
1. **Research Phase**: Research agent gathers key insights and sources
2. **Writing Phase**: Writer agent creates structured content
3. **Review Phase**: Reviewer agent assesses quality
4. **Revision Loop**: If quality < threshold, iterate with improvements

**Output**: High-quality, reviewed content with full metrics

---

## Requirements

All dependencies are managed via the project's main configuration. These examples use:

- **Core Framework**: All `src/` modules
- **Observability**: structured_logging, metrics
- **Reliability**: retry, circuit_breaker, timeout
- **Optimization**: cost_tracker, caching
- **Memory**: session_memory
- **Coordination**: a2a_protocol, message_broker, orchestration_patterns

No additional dependencies are required beyond the project setup.

---

## Key Features Demonstrated

### Observability
```python
# Structured logging with context
logger.info("Task completed", duration_ms=100, cost_usd=0.05)

# Metrics collection
metrics.record_llm_tokens(agent_id="agent-1", model="gpt-4", ...)
```

### Reliability
```python
# Automatic retry with exponential backoff
@retry(max_attempts=3, exponential_base=2.0)
async def make_llm_call(prompt: str) -> str:
    ...

# Circuit breaker protection
if circuit_breaker.is_open():
    # Use fallback strategy
```

### Cost Optimization
```python
# Automatic cost tracking
cost_tracker.record_llm_call(
    model_name="gpt-4-turbo",
    input_tokens=100,
    output_tokens=50
)

# Budget management
budget_status = cost_tracker.get_budget_status()
```

### Multi-Agent Coordination
```python
# A2A messaging
message = A2AMessage(
    from_agent_id="agent-1",
    to_agent_id="agent-2",
    message_type=MessageType.TASK_ASSIGNMENT,
    payload={"task": "analyze data"}
)
await broker.publish(message)
```

---

## Customization

You can modify these examples to:

1. **Change the topic**: Edit `WorkflowConfig(topic="Your Topic Here")`
2. **Adjust quality threshold**: Set `quality_threshold=0.8` for stricter reviews
3. **Modify budget**: Change `cost_budget_usd=10.0` to your limits
4. **Add more agents**: Extend the workflow with additional specialized agents
5. **Test different models**: Update `model_name="gpt-4-turbo"` to compare costs

---

## Performance Benchmarks

From our test runs:

| Metric | Basic Agent | Production Agent |
|--------|-------------|------------------|
| Cost Tracking | ✗ None | ✓ $0.0046 tracked |
| Error Handling | ✗ Fails silently | ✓ Retry + CB |
| Observability | ✗ No logs | ✓ Full metrics |
| Memory | ✗ Stateless | ✓ 1 session |
| Quality | ✗ No validation | ✓ Scored 1.00 |

Multi-Agent Workflow:
- Total Cost: $0.010 for complete workflow
- Duration: ~0.65s for research + write + review
- Quality: 1.00/1.00 (passed threshold)
- Revisions: 0 (content approved first time)

---

## Troubleshooting

**Import errors**:
- Make sure you're running from the project root
- Verify `src/` directory exists with all modules

**Module not found**:
- Check that all dependencies are installed
- Run from the project root directory

**Cost tracking shows $0.00**:
- This is expected for simulated LLM calls
- Real API calls will show actual costs

---

## Next Steps

After running these examples:

1. **Review the code**: Each example has detailed comments explaining every improvement
2. **Modify for your use case**: Adapt the patterns to your specific needs
3. **Add real LLM calls**: Replace simulated calls with actual API calls
4. **Deploy to production**: Use these patterns as templates for production agents
5. **Monitor in production**: Use the observability features to track real-world performance

---

## Questions?

These examples demonstrate production-ready patterns used by teams building reliable, cost-effective AI agent systems. Each improvement addresses real pain points experienced in production deployments.

For more details on specific modules, see the main project documentation.
