"""
Tests for Microsoft Advertising Agent
"""

import pytest
from agents.saas_agents.bing_ads.agent import BingAdsAgent, bing_ads_agent


class TestBingAdsAgent:
    """Test suite for Microsoft Advertising Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BingAdsAgent()
        assert agent.agent_id == "agent_599"
        assert agent.role == "Microsoft Advertising Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BingAdsAgent()
        result = agent.execute("test task")
        assert "Microsoft Advertising Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BingAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BingAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_599"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bing_ads_agent.agent_id == "agent_599"


class TestBingAdsIntegration:
    """Integration tests for Microsoft Advertising Agent"""

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