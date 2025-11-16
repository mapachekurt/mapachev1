"""
Tests for LinkedIn Ads Agent
"""

import pytest
from agents.saas_agents.linkedin_ads.agent import LinkedinAdsAgent, linkedin_ads_agent


class TestLinkedinAdsAgent:
    """Test suite for LinkedIn Ads Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LinkedinAdsAgent()
        assert agent.agent_id == "agent_594"
        assert agent.role == "LinkedIn Ads Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "advertising"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LinkedinAdsAgent()
        result = agent.execute("test task")
        assert "LinkedIn Ads Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LinkedinAdsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LinkedinAdsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_594"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "advertising"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert linkedin_ads_agent.agent_id == "agent_594"


class TestLinkedinAdsIntegration:
    """Integration tests for LinkedIn Ads Agent"""

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