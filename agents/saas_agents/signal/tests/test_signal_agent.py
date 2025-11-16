"""
Tests for Signal Agent
"""

import pytest
from agents.saas_agents.signal.agent import SignalAgent, signal_agent


class TestSignalAgent:
    """Test suite for Signal Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SignalAgent()
        assert agent.agent_id == "agent_833"
        assert agent.role == "Signal Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SignalAgent()
        result = agent.execute("test task")
        assert "Signal Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SignalAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SignalAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_833"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert signal_agent.agent_id == "agent_833"


class TestSignalIntegration:
    """Integration tests for Signal Agent"""

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