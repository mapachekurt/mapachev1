"""
Tests for ShipStation Agent
"""

import pytest
from agents.saas_agents.shipstation.agent import ShipstationAgent, shipstation_agent


class TestShipstationAgent:
    """Test suite for ShipStation Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ShipstationAgent()
        assert agent.agent_id == "agent_1112"
        assert agent.role == "ShipStation Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "logistics"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ShipstationAgent()
        result = agent.execute("test task")
        assert "ShipStation Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ShipstationAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ShipstationAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1112"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "logistics"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert shipstation_agent.agent_id == "agent_1112"


class TestShipstationIntegration:
    """Integration tests for ShipStation Agent"""

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