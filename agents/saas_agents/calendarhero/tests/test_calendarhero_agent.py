"""
Tests for Calendar Hero Agent
"""

import pytest
from agents.saas_agents.calendarhero.agent import CalendarheroAgent, calendarhero_agent


class TestCalendarheroAgent:
    """Test suite for Calendar Hero Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CalendarheroAgent()
        assert agent.agent_id == "agent_859"
        assert agent.role == "Calendar Hero Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CalendarheroAgent()
        result = agent.execute("test task")
        assert "Calendar Hero Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CalendarheroAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CalendarheroAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_859"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert calendarhero_agent.agent_id == "agent_859"


class TestCalendarheroIntegration:
    """Integration tests for Calendar Hero Agent"""

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