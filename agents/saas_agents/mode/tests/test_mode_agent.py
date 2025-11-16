"""
Tests for Mode Analytics Agent
"""

import pytest
from agents.saas_agents.mode.agent import ModeAgent, mode_agent


class TestModeAgent:
    """Test suite for Mode Analytics Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ModeAgent()
        assert agent.agent_id == "agent_1355"
        assert agent.role == "Mode Analytics Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ModeAgent()
        result = agent.execute("test task")
        assert "Mode Analytics Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ModeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ModeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1355"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mode_agent.agent_id == "agent_1355"


class TestModeIntegration:
    """Integration tests for Mode Analytics Agent"""

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