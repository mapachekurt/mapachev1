"""
Tests for MediaWiki Agent
"""

import pytest
from agents.saas_agents.mediawiki.agent import MediawikiAgent, mediawiki_agent


class TestMediawikiAgent:
    """Test suite for MediaWiki Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MediawikiAgent()
        assert agent.agent_id == "agent_781"
        assert agent.role == "MediaWiki Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MediawikiAgent()
        result = agent.execute("test task")
        assert "MediaWiki Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MediawikiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MediawikiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_781"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mediawiki_agent.agent_id == "agent_781"


class TestMediawikiIntegration:
    """Integration tests for MediaWiki Agent"""

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