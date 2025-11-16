"""
Tests for Facebook Ads Agent
"""

import pytest
from agents.saas_agents.facebook_ads.agent import FacebookAdsAgent, facebook_ads_agent


class TestFacebookAdsAgent:
    """Test suite for Facebook Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FacebookAdsAgent()
        assert agent.agent_id == "agent_593"
        assert agent.role == "Facebook Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FacebookAdsAgent()
        result = agent.execute("test task")
        assert "Facebook Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FacebookAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FacebookAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_593"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert facebook_ads_agent.agent_id == "agent_593"


class TestFacebookAdsIntegration:
    """Integration tests for Facebook Ads Agent"""

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