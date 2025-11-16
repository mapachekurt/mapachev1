"""
Tests for Grenadine Event Manager Agent
"""

import pytest
from agents.saas_agents.grenadine.agent import GrenadineAgent, grenadine_agent


class TestGrenadineAgent:
    """Test suite for Grenadine Event Manager Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GrenadineAgent()
        assert agent.agent_id == "agent_1218"
        assert agent.role == "Grenadine Event Manager Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GrenadineAgent()
        result = agent.execute("test task")
        assert "Grenadine Event Manager Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GrenadineAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GrenadineAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1218"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert grenadine_agent.agent_id == "agent_1218"


class TestGrenadineIntegration:
    """Integration tests for Grenadine Event Manager Agent"""

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