"""
Tests for Azure CDN Agent
"""

import pytest
from agents.saas_agents.azure_cdn.agent import AzureCdnAgent, azure_cdn_agent


class TestAzureCdnAgent:
    """Test suite for Azure CDN Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureCdnAgent()
        assert agent.agent_id == "agent_657"
        assert agent.role == "Azure CDN Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureCdnAgent()
        result = agent.execute("test task")
        assert "Azure CDN Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureCdnAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureCdnAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_657"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_cdn_agent.agent_id == "agent_657"


class TestAzureCdnIntegration:
    """Integration tests for Azure CDN Agent"""

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