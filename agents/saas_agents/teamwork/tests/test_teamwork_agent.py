"""
Tests for Teamwork Agent
"""

import pytest
from agents.saas_agents.teamwork.agent import TeamworkAgent, teamwork_agent


class TestTeamworkAgent:
    """Test suite for Teamwork Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TeamworkAgent()
        assert agent.agent_id == "agent_805"
        assert agent.role == "Teamwork Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TeamworkAgent()
        result = agent.execute("test task")
        assert "Teamwork Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TeamworkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TeamworkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_805"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert teamwork_agent.agent_id == "agent_805"


class TestTeamworkIntegration:
    """Integration tests for Teamwork Agent"""

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