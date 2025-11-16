"""
Tests for Sprout Social Agent
"""

import pytest
from agents.saas_agents.sprout_social.agent import SproutSocialAgent, sprout_social_agent


class TestSproutSocialAgent:
    """Test suite for Sprout Social Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SproutSocialAgent()
        assert agent.agent_id == "agent_544"
        assert agent.role == "Sprout Social Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "social_media"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SproutSocialAgent()
        result = agent.execute("test task")
        assert "Sprout Social Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SproutSocialAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SproutSocialAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_544"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "social_media"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sprout_social_agent.agent_id == "agent_544"


class TestSproutSocialIntegration:
    """Integration tests for Sprout Social Agent"""

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