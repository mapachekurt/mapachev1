"""
Tests for Wiki.js Agent
"""

import pytest
from agents.saas_agents.wiki_js.agent import WikiJsAgent, wiki_js_agent


class TestWikiJsAgent:
    """Test suite for Wiki.js Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WikiJsAgent()
        assert agent.agent_id == "agent_779"
        assert agent.role == "Wiki.js Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WikiJsAgent()
        result = agent.execute("test task")
        assert "Wiki.js Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WikiJsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WikiJsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_779"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wiki_js_agent.agent_id == "agent_779"


class TestWikiJsIntegration:
    """Integration tests for Wiki.js Agent"""

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