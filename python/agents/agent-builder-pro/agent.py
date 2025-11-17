"""
Agent Builder Pro - Main Agent Implementation

RAG-enhanced multi-agent system for building production-ready ADK agents.

This module contains the root SequentialAgent that coordinates 5 specialized
sub-agents through a complete agent development pipeline.

Architecture:
- Root: Sequential Agent (gemini-1.5-pro) with RAG
- Pipeline: Requirements → Architecture → Tools → Code → Validation
- RAG: Gemini File Search corpus with ADK knowledge base

Usage:
    from python.agents.agent_builder_pro import agent_builder_pro_root

    result = agent_builder_pro_root.execute(
        "Build a customer service agent for e-commerce"
    )

    Or with AdkApp:

    from python.agents.agent_builder_pro import create_agent_builder_pro
    from vertexai.agent_engines import AdkApp

    agent = create_agent_builder_pro(corpus_resource_name="...")
    app = AdkApp(agent=agent)
"""

import os
from google.adk import Agent, SequentialAgent
from typing import Optional, Dict, Any

from .sub_agents import (
    requirements_gatherer_agent,
    architecture_designer_agent,
    tool_specification_agent,
    code_generator_agent,
    validation_deployment_agent,
)


def create_agent_builder_pro(
    model: str = "gemini-1.5-pro",
    corpus_resource_name: Optional[str] = None,
    enable_rag: bool = True,
    **kwargs
) -> SequentialAgent:
    """
    Create and configure Agent Builder Pro with RAG capabilities.

    Args:
        model: Model to use for root agent (default: gemini-1.5-pro)
        corpus_resource_name: RAG corpus resource name for knowledge base
        enable_rag: Whether to enable RAG integration (default: True)
        **kwargs: Additional configuration parameters

    Returns:
        Configured SequentialAgent instance with RAG and sub-agents

    Example:
        >>> agent = create_agent_builder_pro(
        ...     corpus_resource_name="projects/my-project/locations/us-central1/corpora/adk-kb"
        ... )
        >>> result = agent.execute("Build a data analysis agent")
    """
    # Build tool configuration for RAG
    tool_config = {}
    if enable_rag and corpus_resource_name:
        tool_config["file_search"] = {
            "corpus_resource_name": corpus_resource_name
        }

    # Root agent instruction
    root_instruction = """You are Agent Builder Pro, an expert system for building sophisticated ADK agents.

Your mission is to guide developers through the complete agent development lifecycle,
from requirements gathering to production deployment.

CAPABILITIES:
- Comprehensive ADK knowledge through RAG-enhanced knowledge base
- Expert guidance on agent patterns (Sequential, Parallel, Loop, Hierarchical)
- Production-ready code generation with best practices
- Tool integration expertise (MCP, Python functions, RAG)
- Deployment automation for Vertex AI Agent Engine

WORKFLOW:
You coordinate 5 specialized sub-agents in a sequential pipeline:

1. **Requirements Gatherer** - Analyzes and structures requirements
   - Identifies agent type and use case
   - Extracts functional and non-functional requirements
   - Defines success criteria

2. **Architecture Designer** - Designs optimal agent architecture
   - Selects appropriate agent pattern
   - Defines sub-agent structure
   - Plans data flow and integrations

3. **Tool Specification** - Defines tool integrations
   - Specifies tool interfaces
   - Plans error handling
   - Validates tool availability

4. **Code Generator** - Generates production-ready code
   - Creates complete agent implementation
   - Follows ADK best practices
   - Includes comprehensive documentation

5. **Validation & Deployment** - Validates and prepares deployment
   - Reviews code quality
   - Creates deployment scripts
   - Generates test plans

IMPORTANT GUIDELINES:

**Knowledge Base Usage:**
- Use your RAG knowledge base to provide accurate, up-to-date ADK information
- Always cite sources when referencing best practices or patterns
- Reference code examples from the knowledge base
- Verify pattern appropriateness using documented use cases

**Best Practices:**
- Follow ADK patterns and conventions
- Generate production-ready code (error handling, logging, documentation)
- Consider model selection (Flash for sub-agents, Pro for complex reasoning)
- Implement security best practices (secrets management, input validation)
- Plan for scalability and maintainability
- Include comprehensive testing

**Code Quality:**
- Full type hints throughout
- Comprehensive docstrings (Google style)
- Proper error handling with try-except blocks
- Logging at key points
- No hardcoded secrets (use environment variables)
- Clean, readable code structure

**Output Structure:**
For each agent building request, coordinate your sub-agents to provide:
1. ✓ Requirements Analysis Document
2. ✓ Architecture Specification
3. ✓ Tool Specifications
4. ✓ Complete Code Implementation
5. ✓ Deployment Package (tests, scripts, docs)

**Communication Style:**
- Be clear and professional
- Provide rationale for decisions
- Cite knowledge base sources
- Offer alternatives when appropriate
- Explain tradeoffs (cost, performance, complexity)

Remember: You're building agents that will run in production. Quality, security,
and maintainability are paramount.
"""

    # Create root Sequential Agent
    root_agent = SequentialAgent(
        name="agent_builder_pro",
        instruction=root_instruction,
        model=model,
        sub_agents=[
            requirements_gatherer_agent,
            architecture_designer_agent,
            tool_specification_agent,
            code_generator_agent,
            validation_deployment_agent,
        ],
        tool_config=tool_config if tool_config else None,
    )

    return root_agent


def create_agent_builder_pro_with_config(config: Dict[str, Any]) -> SequentialAgent:
    """
    Create Agent Builder Pro from configuration dictionary.

    Args:
        config: Configuration dictionary with keys:
            - model: str (optional)
            - corpus_resource_name: str (optional)
            - enable_rag: bool (optional)

    Returns:
        Configured SequentialAgent instance
    """
    return create_agent_builder_pro(
        model=config.get("model", "gemini-1.5-pro"),
        corpus_resource_name=config.get("corpus_resource_name"),
        enable_rag=config.get("enable_rag", True),
    )


# Create default instance with environment-based configuration
agent_builder_pro_root = create_agent_builder_pro(
    corpus_resource_name=os.getenv("ADK_CORPUS_RESOURCE_NAME"),
    enable_rag=os.getenv("ENABLE_RAG", "true").lower() == "true",
)


# Convenience functions for common use cases
def build_customer_service_agent(domain: str = "general") -> str:
    """
    Build a customer service agent for a specific domain.

    Args:
        domain: Business domain (e.g., "e-commerce", "saas", "healthcare")

    Returns:
        Agent implementation code and deployment package
    """
    prompt = f"Build a customer service agent for {domain} that handles inquiries, complaints, and support requests."
    return agent_builder_pro_root.execute(prompt)


def build_data_analysis_agent(data_sources: str = "databases") -> str:
    """
    Build a data analysis agent.

    Args:
        data_sources: Data sources to analyze (e.g., "databases", "APIs", "files")

    Returns:
        Agent implementation code and deployment package
    """
    prompt = f"Build a data analysis agent that processes data from {data_sources}, performs analysis, and generates insights."
    return agent_builder_pro_root.execute(prompt)


def build_automation_agent(tasks: str) -> str:
    """
    Build an automation agent for specific tasks.

    Args:
        tasks: Tasks to automate (description)

    Returns:
        Agent implementation code and deployment package
    """
    prompt = f"Build an automation agent for: {tasks}"
    return agent_builder_pro_root.execute(prompt)


# Export public API
__all__ = [
    "create_agent_builder_pro",
    "create_agent_builder_pro_with_config",
    "agent_builder_pro_root",
    "build_customer_service_agent",
    "build_data_analysis_agent",
    "build_automation_agent",
]
