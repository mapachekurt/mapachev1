"""
Tests for Mixmax Agent
"""

import pytest
from agents.saas_agents.mixmax.agent import MixmaxAgent, mixmax_agent


class TestMixmaxAgent:
    """Test suite for Mixmax Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MixmaxAgent()
        assert agent.agent_id == "agent_858"
        assert agent.role == "Mixmax Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MixmaxAgent()
        result = agent.execute("test task")
        assert "Mixmax Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MixmaxAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MixmaxAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_858"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mixmax_agent.agent_id == "agent_858"


class TestMixmaxIntegration:
    """Integration tests for Mixmax Agent"""

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