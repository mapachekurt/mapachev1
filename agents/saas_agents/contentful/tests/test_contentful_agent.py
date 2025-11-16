"""
Tests for Contentful Agent
"""

import pytest
from agents.saas_agents.contentful.agent import ContentfulAgent, contentful_agent


class TestContentfulAgent:
    """Test suite for Contentful Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ContentfulAgent()
        assert agent.agent_id == "agent_602"
        assert agent.role == "Contentful Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "content_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ContentfulAgent()
        result = agent.execute("test task")
        assert "Contentful Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ContentfulAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ContentfulAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_602"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "content_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert contentful_agent.agent_id == "agent_602"


class TestContentfulIntegration:
    """Integration tests for Contentful Agent"""

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