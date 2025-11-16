"""
Tests for Ubersuggest Agent
"""

import pytest
from agents.saas_agents.ubersuggest.agent import UbersuggestAgent, ubersuggest_agent


class TestUbersuggestAgent:
    """Test suite for Ubersuggest Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = UbersuggestAgent()
        assert agent.agent_id == "agent_561"
        assert agent.role == "Ubersuggest Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "seo"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = UbersuggestAgent()
        result = agent.execute("test task")
        assert "Ubersuggest Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = UbersuggestAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = UbersuggestAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_561"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "seo"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ubersuggest_agent.agent_id == "agent_561"


class TestUbersuggestIntegration:
    """Integration tests for Ubersuggest Agent"""

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