"""
Tests for Quizizz Agent
"""

import pytest
from agents.saas_agents.quizizz.agent import QuizizzAgent, quizizz_agent


class TestQuizizzAgent:
    """Test suite for Quizizz Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = QuizizzAgent()
        assert agent.agent_id == "agent_1064"
        assert agent.role == "Quizizz Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = QuizizzAgent()
        result = agent.execute("test task")
        assert "Quizizz Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = QuizizzAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = QuizizzAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1064"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert quizizz_agent.agent_id == "agent_1064"


class TestQuizizzIntegration:
    """Integration tests for Quizizz Agent"""

    @pytest.mark.skip(reason="Requires live API credentials")
    def test_api_connection(self):
        """Test API connection (requires credentials)"""
        # TODO: Implement when API credentials available
        pass

    @pytest.mark.skip(reason="Requires MCP server")
    def test_mcp_integration(self):
        """Test MCP server integration"""
        # TODO: Implement when MCP server available
        pass