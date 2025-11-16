"""
Tests for Sendible Agent
"""

import pytest
from agents.saas_agents.sendible.agent import SendibleAgent, sendible_agent


class TestSendibleAgent:
    """Test suite for Sendible Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SendibleAgent()
        assert agent.agent_id == "agent_550"
        assert agent.role == "Sendible Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "social_media"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SendibleAgent()
        result = agent.execute("test task")
        assert "Sendible Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SendibleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SendibleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_550"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "social_media"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sendible_agent.agent_id == "agent_550"


class TestSendibleIntegration:
    """Integration tests for Sendible Agent"""

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