"""
Tests for Later Agent
"""

import pytest
from agents.saas_agents.later.agent import LaterAgent, later_agent


class TestLaterAgent:
    """Test suite for Later Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LaterAgent()
        assert agent.agent_id == "agent_545"
        assert agent.role == "Later Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "social_media"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LaterAgent()
        result = agent.execute("test task")
        assert "Later Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LaterAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LaterAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_545"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "social_media"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert later_agent.agent_id == "agent_545"


class TestLaterIntegration:
    """Integration tests for Later Agent"""

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