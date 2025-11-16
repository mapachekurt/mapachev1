"""
Tests for Dialpad Agent
"""

import pytest
from agents.saas_agents.dialpad.agent import DialpadAgent, dialpad_agent


class TestDialpadAgent:
    """Test suite for Dialpad Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DialpadAgent()
        assert agent.agent_id == "agent_871"
        assert agent.role == "Dialpad Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DialpadAgent()
        result = agent.execute("test task")
        assert "Dialpad Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DialpadAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DialpadAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_871"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dialpad_agent.agent_id == "agent_871"


class TestDialpadIntegration:
    """Integration tests for Dialpad Agent"""

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