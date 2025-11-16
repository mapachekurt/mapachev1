"""
Tests for Autopilot Agent
"""

import pytest
from agents.saas_agents.autopilot.agent import AutopilotAgent, autopilot_agent


class TestAutopilotAgent:
    """Test suite for Autopilot Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AutopilotAgent()
        assert agent.agent_id == "agent_585"
        assert agent.role == "Autopilot Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "marketing_automation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AutopilotAgent()
        result = agent.execute("test task")
        assert "Autopilot Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AutopilotAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AutopilotAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_585"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "marketing_automation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert autopilot_agent.agent_id == "agent_585"


class TestAutopilotIntegration:
    """Integration tests for Autopilot Agent"""

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