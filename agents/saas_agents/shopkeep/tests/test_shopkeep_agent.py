"""
Tests for ShopKeep Agent
"""

import pytest
from agents.saas_agents.shopkeep.agent import ShopkeepAgent, shopkeep_agent


class TestShopkeepAgent:
    """Test suite for ShopKeep Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ShopkeepAgent()
        assert agent.agent_id == "agent_1169"
        assert agent.role == "ShopKeep Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ShopkeepAgent()
        result = agent.execute("test task")
        assert "ShopKeep Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ShopkeepAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ShopkeepAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1169"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert shopkeep_agent.agent_id == "agent_1169"


class TestShopkeepIntegration:
    """Integration tests for ShopKeep Agent"""

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