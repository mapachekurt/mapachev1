"""
Tests for Azure Repos Agent
"""

import pytest
from agents.saas_agents.azure_repos.agent import AzureReposAgent, azure_repos_agent


class TestAzureReposAgent:
    """Test suite for Azure Repos Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureReposAgent()
        assert agent.agent_id == "agent_726"
        assert agent.role == "Azure Repos Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "version_control"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureReposAgent()
        result = agent.execute("test task")
        assert "Azure Repos Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureReposAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureReposAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_726"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "version_control"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_repos_agent.agent_id == "agent_726"


class TestAzureReposIntegration:
    """Integration tests for Azure Repos Agent"""

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