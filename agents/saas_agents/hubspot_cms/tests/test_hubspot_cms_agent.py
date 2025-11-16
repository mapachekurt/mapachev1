"""
Tests for HubSpot CMS Agent
"""

import pytest
from agents.saas_agents.hubspot_cms.agent import HubspotCmsAgent, hubspot_cms_agent


class TestHubspotCmsAgent:
    """Test suite for HubSpot CMS Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HubspotCmsAgent()
        assert agent.agent_id == "agent_609"
        assert agent.role == "HubSpot CMS Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "content_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HubspotCmsAgent()
        result = agent.execute("test task")
        assert "HubSpot CMS Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HubspotCmsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HubspotCmsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_609"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "content_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hubspot_cms_agent.agent_id == "agent_609"


class TestHubspotCmsIntegration:
    """Integration tests for HubSpot CMS Agent"""

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