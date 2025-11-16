"""
Tests for TeamCity Agent
"""

import pytest
from agents.saas_agents.teamcity.agent import TeamcityAgent, teamcity_agent


class TestTeamcityAgent:
    """Test suite for TeamCity Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TeamcityAgent()
        assert agent.agent_id == "agent_628"
        assert agent.role == "TeamCity Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "ci_cd"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TeamcityAgent()
        result = agent.execute("test task")
        assert "TeamCity Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TeamcityAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TeamcityAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_628"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "ci_cd"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert teamcity_agent.agent_id == "agent_628"


class TestTeamcityIntegration:
    """Integration tests for TeamCity Agent"""

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