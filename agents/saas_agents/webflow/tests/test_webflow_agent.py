"""
Tests for Webflow Agent
"""

import pytest
from agents.saas_agents.webflow.agent import WebflowAgent, webflow_agent


class TestWebflowAgent:
    """Test suite for Webflow Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WebflowAgent()
        assert agent.agent_id == "agent_606"
        assert agent.role == "Webflow Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "content_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WebflowAgent()
        result = agent.execute("test task")
        assert "Webflow Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WebflowAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WebflowAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_606"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "content_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert webflow_agent.agent_id == "agent_606"


class TestWebflowIntegration:
    """Integration tests for Webflow Agent"""

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