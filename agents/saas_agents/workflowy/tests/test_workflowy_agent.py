"""
Tests for Workflowy Agent
"""

import pytest
from agents.saas_agents.workflowy.agent import WorkflowyAgent, workflowy_agent


class TestWorkflowyAgent:
    """Test suite for Workflowy Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WorkflowyAgent()
        assert agent.agent_id == "agent_756"
        assert agent.role == "Workflowy Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "notes"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WorkflowyAgent()
        result = agent.execute("test task")
        assert "Workflowy Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WorkflowyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WorkflowyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_756"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "notes"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert workflowy_agent.agent_id == "agent_756"


class TestWorkflowyIntegration:
    """Integration tests for Workflowy Agent"""

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