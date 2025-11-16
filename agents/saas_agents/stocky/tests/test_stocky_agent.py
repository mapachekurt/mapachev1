"""
Tests for Stocky Agent
"""

import pytest
from agents.saas_agents.stocky.agent import StockyAgent, stocky_agent


class TestStockyAgent:
    """Test suite for Stocky Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = StockyAgent()
        assert agent.agent_id == "agent_1143"
        assert agent.role == "Stocky Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = StockyAgent()
        result = agent.execute("test task")
        assert "Stocky Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = StockyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = StockyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1143"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert stocky_agent.agent_id == "agent_1143"


class TestStockyIntegration:
    """Integration tests for Stocky Agent"""

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