"""
Tests for ShipMonk Agent
"""

import pytest
from agents.saas_agents.shipmonk.agent import ShipmonkAgent, shipmonk_agent


class TestShipmonkAgent:
    """Test suite for ShipMonk Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ShipmonkAgent()
        assert agent.agent_id == "agent_1127"
        assert agent.role == "ShipMonk Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "logistics"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ShipmonkAgent()
        result = agent.execute("test task")
        assert "ShipMonk Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ShipmonkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ShipmonkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1127"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "logistics"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert shipmonk_agent.agent_id == "agent_1127"


class TestShipmonkIntegration:
    """Integration tests for ShipMonk Agent"""

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