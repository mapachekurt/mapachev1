"""
Tests for Yelp Reservations Agent
"""

import pytest
from agents.saas_agents.yelp_reservations.agent import YelpReservationsAgent, yelp_reservations_agent


class TestYelpReservationsAgent:
    """Test suite for Yelp Reservations Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = YelpReservationsAgent()
        assert agent.agent_id == "agent_1194"
        assert agent.role == "Yelp Reservations Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = YelpReservationsAgent()
        result = agent.execute("test task")
        assert "Yelp Reservations Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = YelpReservationsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = YelpReservationsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1194"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert yelp_reservations_agent.agent_id == "agent_1194"


class TestYelpReservationsIntegration:
    """Integration tests for Yelp Reservations Agent"""

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