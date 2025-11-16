"""
Tests for Rocket.Chat Agent
"""

import pytest
from agents.saas_agents.rocketchat.agent import RocketchatAgent, rocketchat_agent


class TestRocketchatAgent:
    """Test suite for Rocket.Chat Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RocketchatAgent()
        assert agent.agent_id == "agent_838"
        assert agent.role == "Rocket.Chat Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RocketchatAgent()
        result = agent.execute("test task")
        assert "Rocket.Chat Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RocketchatAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RocketchatAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_838"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rocketchat_agent.agent_id == "agent_838"


class TestRocketchatIntegration:
    """Integration tests for Rocket.Chat Agent"""

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