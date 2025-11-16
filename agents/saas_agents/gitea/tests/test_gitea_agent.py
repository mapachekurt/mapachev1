"""
Tests for Gitea Agent
"""

import pytest
from agents.saas_agents.gitea.agent import GiteaAgent, gitea_agent


class TestGiteaAgent:
    """Test suite for Gitea Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GiteaAgent()
        assert agent.agent_id == "agent_727"
        assert agent.role == "Gitea Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "version_control"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GiteaAgent()
        result = agent.execute("test task")
        assert "Gitea Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GiteaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GiteaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_727"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "version_control"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gitea_agent.agent_id == "agent_727"


class TestGiteaIntegration:
    """Integration tests for Gitea Agent"""

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