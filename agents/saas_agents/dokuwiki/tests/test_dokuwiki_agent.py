"""
Tests for DokuWiki Agent
"""

import pytest
from agents.saas_agents.dokuwiki.agent import DokuwikiAgent, dokuwiki_agent


class TestDokuwikiAgent:
    """Test suite for DokuWiki Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DokuwikiAgent()
        assert agent.agent_id == "agent_780"
        assert agent.role == "DokuWiki Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DokuwikiAgent()
        result = agent.execute("test task")
        assert "DokuWiki Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DokuwikiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DokuwikiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_780"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dokuwiki_agent.agent_id == "agent_780"


class TestDokuwikiIntegration:
    """Integration tests for DokuWiki Agent"""

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