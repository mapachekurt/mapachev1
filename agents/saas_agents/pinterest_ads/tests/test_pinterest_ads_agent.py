"""
Tests for Pinterest Ads Agent
"""

import pytest
from agents.saas_agents.pinterest_ads.agent import PinterestAdsAgent, pinterest_ads_agent


class TestPinterestAdsAgent:
    """Test suite for Pinterest Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PinterestAdsAgent()
        assert agent.agent_id == "agent_597"
        assert agent.role == "Pinterest Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PinterestAdsAgent()
        result = agent.execute("test task")
        assert "Pinterest Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PinterestAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PinterestAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_597"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pinterest_ads_agent.agent_id == "agent_597"


class TestPinterestAdsIntegration:
    """Integration tests for Pinterest Ads Agent"""

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