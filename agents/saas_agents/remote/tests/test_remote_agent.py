"""
Tests for Remote.com Agent
"""

import pytest
from agents.saas_agents.remote.agent import RemoteAgent, remote_agent


class TestRemoteAgent:
    """Test suite for Remote.com Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RemoteAgent()
        assert agent.agent_id == "agent_961"
        assert agent.role == "Remote.com Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RemoteAgent()
        result = agent.execute("test task")
        assert "Remote.com Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RemoteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RemoteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_961"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert remote_agent.agent_id == "agent_961"


class TestRemoteIntegration:
    """Integration tests for Remote.com Agent"""

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