"""
Tests for Lightspeed Restaurant Agent
"""

import pytest
from agents.saas_agents.lightspeed_restaurant.agent import LightspeedRestaurantAgent, lightspeed_restaurant_agent


class TestLightspeedRestaurantAgent:
    """Test suite for Lightspeed Restaurant Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LightspeedRestaurantAgent()
        assert agent.agent_id == "agent_1154"
        assert agent.role == "Lightspeed Restaurant Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LightspeedRestaurantAgent()
        result = agent.execute("test task")
        assert "Lightspeed Restaurant Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LightspeedRestaurantAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LightspeedRestaurantAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1154"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lightspeed_restaurant_agent.agent_id == "agent_1154"


class TestLightspeedRestaurantIntegration:
    """Integration tests for Lightspeed Restaurant Agent"""

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