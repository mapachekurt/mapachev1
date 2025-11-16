"""
Tests for Azure DevOps Agent
"""

import pytest
from agents.saas_agents.azure_devops.agent import AzureDevopsAgent, azure_devops_agent


class TestAzureDevopsAgent:
    """Test suite for Azure DevOps Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureDevopsAgent()
        assert agent.agent_id == "agent_632"
        assert agent.role == "Azure DevOps Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "ci_cd"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureDevopsAgent()
        result = agent.execute("test task")
        assert "Azure DevOps Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureDevopsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureDevopsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_632"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "ci_cd"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_devops_agent.agent_id == "agent_632"


class TestAzureDevopsIntegration:
    """Integration tests for Azure DevOps Agent"""

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