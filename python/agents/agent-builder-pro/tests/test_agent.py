"""
Basic tests for Agent Builder Pro.

Run with: pytest python/agents/agent-builder-pro/tests/
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_agent_imports():
    """Test that agent modules can be imported."""
    try:
        from agent import agent_builder_pro_root, create_agent_builder_pro
        assert agent_builder_pro_root is not None
        assert create_agent_builder_pro is not None
    except ImportError as e:
        pytest.fail(f"Failed to import agent: {e}")


def test_agent_structure():
    """Test agent has correct structure."""
    from agent import agent_builder_pro_root

    assert agent_builder_pro_root.name == "agent_builder_pro"
    assert agent_builder_pro_root.model in ["gemini-1.5-pro", "gemini-2.0-flash-001"]

    # Check sub-agents
    if hasattr(agent_builder_pro_root, 'sub_agents'):
        assert len(agent_builder_pro_root.sub_agents) == 5, "Should have 5 sub-agents"


def test_sub_agent_imports():
    """Test that sub-agents can be imported."""
    try:
        from sub_agents import (
            requirements_gatherer_agent,
            architecture_designer_agent,
            tool_specification_agent,
            code_generator_agent,
            validation_deployment_agent,
        )
        assert requirements_gatherer_agent is not None
        assert architecture_designer_agent is not None
        assert tool_specification_agent is not None
        assert code_generator_agent is not None
        assert validation_deployment_agent is not None
    except ImportError as e:
        pytest.fail(f"Failed to import sub-agents: {e}")


def test_agent_creation_with_corpus():
    """Test creating agent with RAG corpus."""
    from agent import create_agent_builder_pro

    test_corpus = "projects/test/locations/us-central1/corpora/test"
    agent = create_agent_builder_pro(
        corpus_resource_name=test_corpus,
        enable_rag=True
    )

    assert agent is not None
    assert hasattr(agent, 'tool_config')

    if agent.tool_config:
        assert "file_search" in agent.tool_config


def test_agent_creation_without_rag():
    """Test creating agent without RAG."""
    from agent import create_agent_builder_pro

    agent = create_agent_builder_pro(enable_rag=False)

    assert agent is not None

    # tool_config should be None or empty when RAG disabled
    if hasattr(agent, 'tool_config') and agent.tool_config:
        assert "file_search" not in agent.tool_config


def test_convenience_functions():
    """Test convenience functions exist and are callable."""
    from agent import (
        build_customer_service_agent,
        build_data_analysis_agent,
        build_automation_agent,
    )

    assert callable(build_customer_service_agent)
    assert callable(build_data_analysis_agent)
    assert callable(build_automation_agent)


# Note: Actual execution tests require runtime and may be expensive
# These are covered by test_rag_agent.py
