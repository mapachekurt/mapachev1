"""
Tests for Inventory Planner Agent
"""

import pytest
from agents.saas_agents.inventory_planner.agent import InventoryPlannerAgent, inventory_planner_agent


class TestInventoryPlannerAgent:
    """Test suite for Inventory Planner Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = InventoryPlannerAgent()
        assert agent.agent_id == "agent_1142"
        assert agent.role == "Inventory Planner Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = InventoryPlannerAgent()
        result = agent.execute("test task")
        assert "Inventory Planner Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = InventoryPlannerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = InventoryPlannerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1142"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert inventory_planner_agent.agent_id == "agent_1142"


class TestInventoryPlannerIntegration:
    """Integration tests for Inventory Planner Agent"""

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