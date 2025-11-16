"""
Tests for TikTok Ads Agent
"""

import pytest
from agents.saas_agents.tiktok_ads.agent import TiktokAdsAgent, tiktok_ads_agent


class TestTiktokAdsAgent:
    """Test suite for TikTok Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TiktokAdsAgent()
        assert agent.agent_id == "agent_596"
        assert agent.role == "TikTok Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TiktokAdsAgent()
        result = agent.execute("test task")
        assert "TikTok Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TiktokAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TiktokAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_596"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert tiktok_ads_agent.agent_id == "agent_596"


class TestTiktokAdsIntegration:
    """Integration tests for TikTok Ads Agent"""

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