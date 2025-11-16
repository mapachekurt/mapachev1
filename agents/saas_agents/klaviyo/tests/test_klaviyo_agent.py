"""
Tests for Klaviyo Agent
"""

import pytest
from agents.saas_agents.klaviyo.agent import KlaviyoAgent, klaviyo_agent


class TestKlaviyoAgent:
    """Test suite for Klaviyo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KlaviyoAgent()
        assert agent.agent_id == "agent_536"
        assert agent.role == "Klaviyo Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KlaviyoAgent()
        result = agent.execute("test task")
        assert "Klaviyo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KlaviyoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KlaviyoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_536"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert klaviyo_agent.agent_id == "agent_536"


class TestKlaviyoIntegration:
    """Integration tests for Klaviyo Agent"""

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