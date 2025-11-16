"""
Tests for Azure DNS Agent
"""

import pytest
from agents.saas_agents.azure_dns.agent import AzureDnsAgent, azure_dns_agent


class TestAzureDnsAgent:
    """Test suite for Azure DNS Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureDnsAgent()
        assert agent.agent_id == "agent_658"
        assert agent.role == "Azure DNS Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureDnsAgent()
        result = agent.execute("test task")
        assert "Azure DNS Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureDnsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureDnsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_658"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_dns_agent.agent_id == "agent_658"


class TestAzureDnsIntegration:
    """Integration tests for Azure DNS Agent"""

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