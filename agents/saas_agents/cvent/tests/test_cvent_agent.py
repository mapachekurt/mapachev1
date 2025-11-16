"""
Tests for Cvent Agent
"""

import pytest
from agents.saas_agents.cvent.agent import CventAgent, cvent_agent


class TestCventAgent:
    """Test suite for Cvent Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CventAgent()
        assert agent.agent_id == "agent_1214"
        assert agent.role == "Cvent Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CventAgent()
        result = agent.execute("test task")
        assert "Cvent Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CventAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CventAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1214"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cvent_agent.agent_id == "agent_1214"


class TestCventIntegration:
    """Integration tests for Cvent Agent"""

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