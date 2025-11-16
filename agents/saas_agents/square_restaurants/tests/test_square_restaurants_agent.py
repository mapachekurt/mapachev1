"""
Tests for Square for Restaurants Agent
"""

import pytest
from agents.saas_agents.square_restaurants.agent import SquareRestaurantsAgent, square_restaurants_agent


class TestSquareRestaurantsAgent:
    """Test suite for Square for Restaurants Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SquareRestaurantsAgent()
        assert agent.agent_id == "agent_1158"
        assert agent.role == "Square for Restaurants Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SquareRestaurantsAgent()
        result = agent.execute("test task")
        assert "Square for Restaurants Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SquareRestaurantsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SquareRestaurantsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1158"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert square_restaurants_agent.agent_id == "agent_1158"


class TestSquareRestaurantsIntegration:
    """Integration tests for Square for Restaurants Agent"""

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