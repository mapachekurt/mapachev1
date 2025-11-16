"""
Tests for WordPress Agent
"""

import pytest
from agents.saas_agents.wordpress.agent import WordpressAgent, wordpress_agent


class TestWordpressAgent:
    """Test suite for WordPress Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WordpressAgent()
        assert agent.agent_id == "agent_603"
        assert agent.role == "WordPress Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "content_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WordpressAgent()
        result = agent.execute("test task")
        assert "WordPress Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WordpressAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WordpressAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_603"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "content_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wordpress_agent.agent_id == "agent_603"


class TestWordpressIntegration:
    """Integration tests for WordPress Agent"""

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