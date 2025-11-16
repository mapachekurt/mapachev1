"""
Tests for GitLab CI/CD Agent
"""

import pytest
from agents.saas_agents.gitlab_ci.agent import GitlabCiAgent, gitlab_ci_agent


class TestGitlabCiAgent:
    """Test suite for GitLab CI/CD Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GitlabCiAgent()
        assert agent.agent_id == "agent_626"
        assert agent.role == "GitLab CI/CD Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "ci_cd"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GitlabCiAgent()
        result = agent.execute("test task")
        assert "GitLab CI/CD Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GitlabCiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GitlabCiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_626"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "ci_cd"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gitlab_ci_agent.agent_id == "agent_626"


class TestGitlabCiIntegration:
    """Integration tests for GitLab CI/CD Agent"""

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