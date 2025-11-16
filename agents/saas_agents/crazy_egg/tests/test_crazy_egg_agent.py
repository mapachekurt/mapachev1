"""
Tests for Crazy Egg Agent
"""

import pytest
from agents.saas_agents.crazy_egg.agent import CrazyEggAgent, crazy_egg_agent


class TestCrazyEggAgent:
    """Test suite for Crazy Egg Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CrazyEggAgent()
        assert agent.agent_id == "agent_568"
        assert agent.role == "Crazy Egg Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "analytics"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CrazyEggAgent()
        result = agent.execute("test task")
        assert "Crazy Egg Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CrazyEggAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CrazyEggAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_568"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "analytics"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert crazy_egg_agent.agent_id == "agent_568"


class TestCrazyEggIntegration:
    """Integration tests for Crazy Egg Agent"""

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