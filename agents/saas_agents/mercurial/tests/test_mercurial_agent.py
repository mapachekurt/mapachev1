"""
Tests for Mercurial Agent
"""

import pytest
from agents.saas_agents.mercurial.agent import MercurialAgent, mercurial_agent


class TestMercurialAgent:
    """Test suite for Mercurial Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MercurialAgent()
        assert agent.agent_id == "agent_724"
        assert agent.role == "Mercurial Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "version_control"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MercurialAgent()
        result = agent.execute("test task")
        assert "Mercurial Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MercurialAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MercurialAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_724"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "version_control"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mercurial_agent.agent_id == "agent_724"


class TestMercurialIntegration:
    """Integration tests for Mercurial Agent"""

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