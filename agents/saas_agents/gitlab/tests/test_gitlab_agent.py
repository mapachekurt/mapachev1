"""
Tests for GitLab Agent
"""

import pytest
from agents.saas_agents.gitlab.agent import GitlabAgent, gitlab_agent


class TestGitlabAgent:
    """Test suite for GitLab Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GitlabAgent()
        assert agent.agent_id == "agent_527"
        assert agent.role == "GitLab Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "development"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GitlabAgent()
        result = agent.execute("test task")
        assert "GitLab Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GitlabAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GitlabAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_527"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "development"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gitlab_agent.agent_id == "agent_527"


class TestGitlabIntegration:
    """Integration tests for GitLab Agent"""

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