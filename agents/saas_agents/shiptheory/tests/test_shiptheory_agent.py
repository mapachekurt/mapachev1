"""
Tests for Shiptheory Agent
"""

import pytest
from agents.saas_agents.shiptheory.agent import ShiptheoryAgent, shiptheory_agent


class TestShiptheoryAgent:
    """Test suite for Shiptheory Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ShiptheoryAgent()
        assert agent.agent_id == "agent_1151"
        assert agent.role == "Shiptheory Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ShiptheoryAgent()
        result = agent.execute("test task")
        assert "Shiptheory Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ShiptheoryAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ShiptheoryAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1151"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert shiptheory_agent.agent_id == "agent_1151"


class TestShiptheoryIntegration:
    """Integration tests for Shiptheory Agent"""

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