"""
Tests for Scheduled Agent
"""

import pytest
from agents.saas_agents.scheduled.agent import ScheduledAgent, scheduled_agent


class TestScheduledAgent:
    """Test suite for Scheduled Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ScheduledAgent()
        assert agent.agent_id == "agent_1512"
        assert agent.role == "Scheduled Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ScheduledAgent()
        result = agent.execute("test task")
        assert "Scheduled Agent executing" in result
        assert "test task" in result

    def test_agent_execute_no_task(self):
        """Test agent execute method with no task"""
        agent = ScheduledAgent()
        result = agent.execute()
        assert "Scheduled Agent ready for operations" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ScheduledAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ScheduledAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1512"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert scheduled_agent.agent_id == "agent_1512"


class TestScheduledIntegration:
    """Integration tests for Scheduled Agent"""

    @pytest.mark.skip(reason="Requires live Google OAuth credentials")
    def test_api_connection(self):
        """Test API connection (requires credentials)"""
        # TODO: Implement when API credentials available
        pass

    @pytest.mark.skip(reason="Requires MCP server")
    def test_mcp_integration(self):
        """Test MCP server integration"""
        # TODO: Implement when MCP server available
        pass
