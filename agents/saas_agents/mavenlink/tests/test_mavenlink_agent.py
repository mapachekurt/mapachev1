"""
Tests for Mavenlink Agent
"""

import pytest
from agents.saas_agents.mavenlink.agent import MavenlinkAgent, mavenlink_agent


class TestMavenlinkAgent:
    """Test suite for Mavenlink Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MavenlinkAgent()
        assert agent.agent_id == "agent_810"
        assert agent.role == "Mavenlink Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MavenlinkAgent()
        result = agent.execute("test task")
        assert "Mavenlink Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MavenlinkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MavenlinkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_810"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mavenlink_agent.agent_id == "agent_810"


class TestMavenlinkIntegration:
    """Integration tests for Mavenlink Agent"""

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