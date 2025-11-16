"""
Tests for Google Ads Agent
"""

import pytest
from agents.saas_agents.google_ads.agent import GoogleAdsAgent, google_ads_agent


class TestGoogleAdsAgent:
    """Test suite for Google Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GoogleAdsAgent()
        assert agent.agent_id == "agent_592"
        assert agent.role == "Google Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GoogleAdsAgent()
        result = agent.execute("test task")
        assert "Google Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GoogleAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GoogleAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_592"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert google_ads_agent.agent_id == "agent_592"


class TestGoogleAdsIntegration:
    """Integration tests for Google Ads Agent"""

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