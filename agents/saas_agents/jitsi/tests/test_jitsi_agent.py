"""
Tests for Jitsi Agent
"""

import pytest
from agents.saas_agents.jitsi.agent import JitsiAgent, jitsi_agent


class TestJitsiAgent:
    """Test suite for Jitsi Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JitsiAgent()
        assert agent.agent_id == "agent_863"
        assert agent.role == "Jitsi Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JitsiAgent()
        result = agent.execute("test task")
        assert "Jitsi Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JitsiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JitsiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_863"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert jitsi_agent.agent_id == "agent_863"


class TestJitsiIntegration:
    """Integration tests for Jitsi Agent"""

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