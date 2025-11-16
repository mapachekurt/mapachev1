"""
Tests for Majestic SEO Agent
"""

import pytest
from agents.saas_agents.majestic.agent import MajesticAgent, majestic_agent


class TestMajesticAgent:
    """Test suite for Majestic SEO Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MajesticAgent()
        assert agent.agent_id == "agent_556"
        assert agent.role == "Majestic SEO Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "seo"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MajesticAgent()
        result = agent.execute("test task")
        assert "Majestic SEO Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MajesticAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MajesticAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_556"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "seo"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert majestic_agent.agent_id == "agent_556"


class TestMajesticIntegration:
    """Integration tests for Majestic SEO Agent"""

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