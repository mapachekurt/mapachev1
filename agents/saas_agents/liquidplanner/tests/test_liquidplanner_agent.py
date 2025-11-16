"""
Tests for LiquidPlanner Agent
"""

import pytest
from agents.saas_agents.liquidplanner.agent import LiquidplannerAgent, liquidplanner_agent


class TestLiquidplannerAgent:
    """Test suite for LiquidPlanner Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LiquidplannerAgent()
        assert agent.agent_id == "agent_813"
        assert agent.role == "LiquidPlanner Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LiquidplannerAgent()
        result = agent.execute("test task")
        assert "LiquidPlanner Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LiquidplannerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LiquidplannerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_813"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert liquidplanner_agent.agent_id == "agent_813"


class TestLiquidplannerIntegration:
    """Integration tests for LiquidPlanner Agent"""

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