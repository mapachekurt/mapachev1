"""
Tests for Adobe Workfront Agent
"""

import pytest
from agents.saas_agents.workfront.agent import WorkfrontAgent, workfront_agent


class TestWorkfrontAgent:
    """Test suite for Adobe Workfront Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WorkfrontAgent()
        assert agent.agent_id == "agent_808"
        assert agent.role == "Adobe Workfront Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WorkfrontAgent()
        result = agent.execute("test task")
        assert "Adobe Workfront Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WorkfrontAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WorkfrontAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_808"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert workfront_agent.agent_id == "agent_808"


class TestWorkfrontIntegration:
    """Integration tests for Adobe Workfront Agent"""

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