"""
Tests for Azure AKS Agent
"""

import pytest
from agents.saas_agents.azure_aks.agent import AzureAksAgent, azure_aks_agent


class TestAzureAksAgent:
    """Test suite for Azure AKS Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureAksAgent()
        assert agent.agent_id == "agent_660"
        assert agent.role == "Azure AKS Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureAksAgent()
        result = agent.execute("test task")
        assert "Azure AKS Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureAksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureAksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_660"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_aks_agent.agent_id == "agent_660"


class TestAzureAksIntegration:
    """Integration tests for Azure AKS Agent"""

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