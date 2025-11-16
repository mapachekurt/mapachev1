"""
Tests for Sellbrite Agent
"""

import pytest
from agents.saas_agents.sellbrite.agent import SellbriteAgent, sellbrite_agent


class TestSellbriteAgent:
    """Test suite for Sellbrite Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SellbriteAgent()
        assert agent.agent_id == "agent_1145"
        assert agent.role == "Sellbrite Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SellbriteAgent()
        result = agent.execute("test task")
        assert "Sellbrite Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SellbriteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SellbriteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1145"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sellbrite_agent.agent_id == "agent_1145"


class TestSellbriteIntegration:
    """Integration tests for Sellbrite Agent"""

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