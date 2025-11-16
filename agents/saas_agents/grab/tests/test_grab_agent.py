"""
Tests for Grab Agent
"""

import pytest
from agents.saas_agents.grab.agent import GrabAgent, grab_agent


class TestGrabAgent:
    """Test suite for Grab Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GrabAgent()
        assert agent.agent_id == "agent_1481"
        assert agent.role == "Grab Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GrabAgent()
        result = agent.execute("test task")
        assert "Grab Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GrabAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GrabAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1481"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert grab_agent.agent_id == "agent_1481"


class TestGrabIntegration:
    """Integration tests for Grab Agent"""

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