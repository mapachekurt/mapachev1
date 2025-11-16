"""
Tests for Craft Agent
"""

import pytest
from agents.saas_agents.craft.agent import CraftAgent, craft_agent


class TestCraftAgent:
    """Test suite for Craft Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CraftAgent()
        assert agent.agent_id == "agent_752"
        assert agent.role == "Craft Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "notes"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CraftAgent()
        result = agent.execute("test task")
        assert "Craft Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CraftAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CraftAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_752"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "notes"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert craft_agent.agent_id == "agent_752"


class TestCraftIntegration:
    """Integration tests for Craft Agent"""

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