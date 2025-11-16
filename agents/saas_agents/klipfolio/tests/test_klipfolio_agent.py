"""
Tests for Klipfolio Agent
"""

import pytest
from agents.saas_agents.klipfolio.agent import KlipfolioAgent, klipfolio_agent


class TestKlipfolioAgent:
    """Test suite for Klipfolio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KlipfolioAgent()
        assert agent.agent_id == "agent_1358"
        assert agent.role == "Klipfolio Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KlipfolioAgent()
        result = agent.execute("test task")
        assert "Klipfolio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KlipfolioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KlipfolioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1358"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert klipfolio_agent.agent_id == "agent_1358"


class TestKlipfolioIntegration:
    """Integration tests for Klipfolio Agent"""

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