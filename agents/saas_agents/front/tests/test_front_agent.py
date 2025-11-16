"""
Tests for Front Agent
"""

import pytest
from agents.saas_agents.front.agent import FrontAgent, front_agent


class TestFrontAgent:
    """Test suite for Front Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FrontAgent()
        assert agent.agent_id == "agent_1008"
        assert agent.role == "Front Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FrontAgent()
        result = agent.execute("test task")
        assert "Front Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FrontAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FrontAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1008"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert front_agent.agent_id == "agent_1008"


class TestFrontIntegration:
    """Integration tests for Front Agent"""

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