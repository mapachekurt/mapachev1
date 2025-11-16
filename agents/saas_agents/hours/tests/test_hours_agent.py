"""
Tests for Hours Agent
"""

import pytest
from agents.saas_agents.hours.agent import HoursAgent, hours_agent


class TestHoursAgent:
    """Test suite for Hours Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HoursAgent()
        assert agent.agent_id == "agent_828"
        assert agent.role == "Hours Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "time_tracking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HoursAgent()
        result = agent.execute("test task")
        assert "Hours Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HoursAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HoursAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_828"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "time_tracking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hours_agent.agent_id == "agent_828"


class TestHoursIntegration:
    """Integration tests for Hours Agent"""

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