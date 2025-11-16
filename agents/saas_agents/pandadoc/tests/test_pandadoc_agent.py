"""
Tests for PandaDoc Agent
"""

import pytest
from agents.saas_agents.pandadoc.agent import PandadocAgent, pandadoc_agent


class TestPandadocAgent:
    """Test suite for PandaDoc Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PandadocAgent()
        assert agent.agent_id == "agent_1318"
        assert agent.role == "PandaDoc Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PandadocAgent()
        result = agent.execute("test task")
        assert "PandaDoc Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PandadocAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PandadocAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1318"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pandadoc_agent.agent_id == "agent_1318"


class TestPandadocIntegration:
    """Integration tests for PandaDoc Agent"""

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