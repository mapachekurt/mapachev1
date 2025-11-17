# Agent Development Kit: Core Agent Types

## Three Main Agent Types

### 1. LLM Agents (`LlmAgent`, `Agent`)

LLM Agents "utilize Large Language Models (LLMs) as their core engine to understand natural language, reason, plan, generate responses, and dynamically decide how to proceed or which tools to use"

**Ideal For:**
- Flexible, language-centric tasks requiring intelligent reasoning
- Dynamic decision-making
- Natural language understanding and generation
- Tool selection and orchestration

**Characteristics:**
- Non-deterministic behavior
- Flexible execution flow
- Model-driven decision making

### 2. Workflow Agents

Workflow agents "control the execution flow of other agents in predefined, deterministic patterns (sequence, parallel, or loop)" without relying on LLM-driven flow control.

**Types:**

#### SequentialAgent
- Executes agents in order, one after another
- Each agent receives output from previous agent
- Perfect for pipelines and multi-step processes
- Use when tasks have dependencies

**Example Use Cases:**
- Data processing pipelines
- Multi-stage analysis
- Ordered task execution
- Agent building workflow (requirements → design → code → test)

#### ParallelAgent
- Executes multiple agents simultaneously
- Independent tasks run concurrently
- Aggregates results from all agents
- Use when tasks are independent

**Example Use Cases:**
- Multi-source data gathering
- Concurrent analysis from different perspectives
- Parallel validation checks
- Multi-channel communication

#### LoopAgent
- Iteratively refines output until criteria met
- Supports max iterations and early stopping
- Perfect for quality improvement cycles
- Use when task requires iterative refinement

**Example Use Cases:**
- Code refinement loops
- Quality improvement iterations
- Test-driven development cycles
- Creative refinement

**Characteristics:**
- Deterministic behavior
- Predictable execution flow
- Predefined logic patterns

### 3. Custom Agents

"Created by extending `BaseAgent` directly, these agents allow you to implement unique operational logic, specific control flows, or specialized integrations"

**Ideal For:**
- Highly tailored requirements
- Specialized workflows
- Custom control flow logic
- Unique integrations

**Characteristics:**
- Variable behavior (your implementation)
- Complete control over execution
- Specialized capabilities

## Key Distinctions

| Aspect | LLM Agent | Workflow Agent | Custom Agent |
|--------|-----------|----------------|--------------|
| **Engine** | Large Language Model | Predefined Logic | Custom Code |
| **Behavior** | Non-deterministic/Flexible | Deterministic/Predictable | Variable |
| **Primary Use** | Language tasks, dynamic decisions | Process orchestration | Specialized workflows |
| **Decision Making** | Model-driven | Rule-based | Developer-defined |
| **Flexibility** | High | Medium | Highest |
| **Predictability** | Low | High | Depends on implementation |

## Multi-Agent Systems

Complex applications combine all three types:
- **LLM agents** handle intelligent execution and decision-making
- **Workflow agents** manage process flow and orchestration
- **Custom agents** provide specialized capabilities

This creates sophisticated, collaborative systems that leverage the strengths of each agent type.

## Foundation: BaseAgent Class

All agents extend from the `BaseAgent` class, the "fundamental blueprint" for ADK agent development across Python, Go, and Java implementations.

**BaseAgent Provides:**
- Core agent interface
- Lifecycle management
- Execution patterns
- Integration points

## Choosing the Right Agent Type

### Use LLM Agent When:
- Task requires natural language understanding
- Decisions should be model-driven
- Flexibility is more important than predictability
- Tool selection should be dynamic

### Use Workflow Agent When:
- Execution flow is well-defined
- Predictability is critical
- Multiple agents need coordination
- Process follows clear patterns (sequential, parallel, loop)

### Use Custom Agent When:
- Standard patterns don't fit your needs
- You need complete control over execution
- Specialized logic is required
- Integration with external systems requires custom code

## Best Practices

1. **Start Simple**: Begin with single LLM agents before moving to multi-agent systems
2. **Layer Appropriately**: Use workflow agents to orchestrate LLM agents
3. **Separate Concerns**: Each agent should have a clear, focused responsibility
4. **Test Independently**: Test each agent before integration
5. **Monitor Behavior**: Track performance and behavior of each agent type differently

## Multi-Agent Architecture Patterns

### Hierarchical Pattern
- Root coordinator agent (Sequential or Parallel)
- Department-level agents (Workflow)
- Task-level agents (LLM)

### Pipeline Pattern
- SequentialAgent root
- Each stage handled by specialized LLM agent
- Clear data flow from stage to stage

### Hub-and-Spoke Pattern
- Central coordinator (LLM agent)
- Parallel execution of specialist agents
- Aggregation and synthesis by coordinator

### Iterative Refinement Pattern
- LoopAgent root
- Generator agent (LLM)
- Reviewer/validator agent (LLM)
- Continues until quality threshold met
