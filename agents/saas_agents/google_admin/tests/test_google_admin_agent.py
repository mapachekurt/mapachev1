"""
Tests for Google Workspace Admin Agent
"""

import pytest
from agents.saas_agents.google_admin.agent import GoogleAdminAgent, google_admin_agent


class TestGoogleAdminAgent:
    """Test suite for Google Workspace Admin Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GoogleAdminAgent()
        assert agent.agent_id == "agent_530"
        assert agent.role == "Google Workspace Admin Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "administration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GoogleAdminAgent()
        result = agent.execute("test task")
        assert "Google Workspace Admin Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GoogleAdminAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GoogleAdminAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_530"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "administration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert google_admin_agent.agent_id == "agent_530"


class TestGoogleAdminIntegration:
    """Integration tests for Google Workspace Admin Agent"""

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