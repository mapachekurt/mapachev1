"""
Tests for SendGrid Advanced Agent
"""

import pytest
from agents.saas_agents.sendgrid_advanced.agent import SendgridAdvancedAgent, sendgrid_advanced_agent


class TestSendgridAdvancedAgent:
    """Test suite for SendGrid Advanced Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SendgridAdvancedAgent()
        assert agent.agent_id == "agent_532"
        assert agent.role == "SendGrid Advanced Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SendgridAdvancedAgent()
        result = agent.execute("test task")
        assert "SendGrid Advanced Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SendgridAdvancedAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SendgridAdvancedAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_532"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sendgrid_advanced_agent.agent_id == "agent_532"


class TestSendgridAdvancedIntegration:
    """Integration tests for SendGrid Advanced Agent"""

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