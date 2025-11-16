"""
Tests for Tavern Agent
"""

import pytest
from agents.saas_agents.tavern.agent import TavernAgent, tavern_agent


class TestTavernAgent:
    """Test suite for Tavern Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TavernAgent()
        assert agent.agent_id == "agent_1398"
        assert agent.role == "Tavern Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TavernAgent()
        result = agent.execute("test task")
        assert "Tavern Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TavernAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TavernAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1398"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert tavern_agent.agent_id == "agent_1398"


class TestTavernIntegration:
    """Integration tests for Tavern Agent"""

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