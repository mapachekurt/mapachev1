"""
Tests for TimeCamp Agent
"""

import pytest
from agents.saas_agents.timecamp.agent import TimecampAgent, timecamp_agent


class TestTimecampAgent:
    """Test suite for TimeCamp Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TimecampAgent()
        assert agent.agent_id == "agent_825"
        assert agent.role == "TimeCamp Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "time_tracking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TimecampAgent()
        result = agent.execute("test task")
        assert "TimeCamp Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TimecampAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TimecampAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_825"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "time_tracking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert timecamp_agent.agent_id == "agent_825"


class TestTimecampIntegration:
    """Integration tests for TimeCamp Agent"""

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