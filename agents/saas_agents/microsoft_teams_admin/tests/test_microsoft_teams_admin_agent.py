"""
Tests for Microsoft Teams Admin Agent
"""

import pytest
from agents.saas_agents.microsoft_teams_admin.agent import MicrosoftTeamsAdminAgent, microsoft_teams_admin_agent


class TestMicrosoftTeamsAdminAgent:
    """Test suite for Microsoft Teams Admin Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MicrosoftTeamsAdminAgent()
        assert agent.agent_id == "agent_529"
        assert agent.role == "Microsoft Teams Admin Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "administration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MicrosoftTeamsAdminAgent()
        result = agent.execute("test task")
        assert "Microsoft Teams Admin Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MicrosoftTeamsAdminAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MicrosoftTeamsAdminAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_529"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "administration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert microsoft_teams_admin_agent.agent_id == "agent_529"


class TestMicrosoftTeamsAdminIntegration:
    """Integration tests for Microsoft Teams Admin Agent"""

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