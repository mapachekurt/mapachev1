"""
Tests for Snapchat Ads Agent
"""

import pytest
from agents.saas_agents.snapchat_ads.agent import SnapchatAdsAgent, snapchat_ads_agent


class TestSnapchatAdsAgent:
    """Test suite for Snapchat Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SnapchatAdsAgent()
        assert agent.agent_id == "agent_598"
        assert agent.role == "Snapchat Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SnapchatAdsAgent()
        result = agent.execute("test task")
        assert "Snapchat Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SnapchatAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SnapchatAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_598"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert snapchat_ads_agent.agent_id == "agent_598"


class TestSnapchatAdsIntegration:
    """Integration tests for Snapchat Ads Agent"""

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