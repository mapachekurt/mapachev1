"""
Tests for Azure Active Directory Agent
"""

import pytest
from agents.saas_agents.azure_ad.agent import AzureAdAgent, azure_ad_agent


class TestAzureAdAgent:
    """Test suite for Azure Active Directory Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureAdAgent()
        assert agent.agent_id == "agent_531"
        assert agent.role == "Azure Active Directory Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "identity"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureAdAgent()
        result = agent.execute("test task")
        assert "Azure Active Directory Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureAdAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureAdAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_531"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "identity"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_ad_agent.agent_id == "agent_531"


class TestAzureAdIntegration:
    """Integration tests for Azure Active Directory Agent"""

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