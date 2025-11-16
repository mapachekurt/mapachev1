"""
Tests for Workable Agent
"""

import pytest
from agents.saas_agents.workable.agent import WorkableAgent, workable_agent


class TestWorkableAgent:
    """Test suite for Workable Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WorkableAgent()
        assert agent.agent_id == "agent_942"
        assert agent.role == "Workable Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WorkableAgent()
        result = agent.execute("test task")
        assert "Workable Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WorkableAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WorkableAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_942"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert workable_agent.agent_id == "agent_942"


class TestWorkableIntegration:
    """Integration tests for Workable Agent"""

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