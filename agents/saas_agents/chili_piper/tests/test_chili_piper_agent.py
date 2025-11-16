"""
Tests for Chili Piper Agent
"""

import pytest
from agents.saas_agents.chili_piper.agent import ChiliPiperAgent, chili_piper_agent


class TestChiliPiperAgent:
    """Test suite for Chili Piper Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ChiliPiperAgent()
        assert agent.agent_id == "agent_857"
        assert agent.role == "Chili Piper Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ChiliPiperAgent()
        result = agent.execute("test task")
        assert "Chili Piper Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ChiliPiperAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ChiliPiperAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_857"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert chili_piper_agent.agent_id == "agent_857"


class TestChiliPiperIntegration:
    """Integration tests for Chili Piper Agent"""

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