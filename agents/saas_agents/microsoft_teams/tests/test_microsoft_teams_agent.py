"""
Tests for Microsoft Teams Agent
"""

import pytest
from agents.saas_agents.microsoft_teams.agent import MicrosoftTeamsAgent, microsoft_teams_agent


class TestMicrosoftTeamsAgent:
    """Test suite for Microsoft Teams Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MicrosoftTeamsAgent()
        assert agent.agent_id == "agent_512"
        assert agent.role == "Microsoft Teams Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MicrosoftTeamsAgent()
        result = agent.execute("test task")
        assert "Microsoft Teams Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MicrosoftTeamsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MicrosoftTeamsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_512"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert microsoft_teams_agent.agent_id == "agent_512"


class TestMicrosoftTeamsIntegration:
    """Integration tests for Microsoft Teams Agent"""

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