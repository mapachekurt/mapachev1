"""
Tests for ProjectManager Agent
"""

import pytest
from agents.saas_agents.projectmanager.agent import ProjectmanagerAgent, projectmanager_agent


class TestProjectmanagerAgent:
    """Test suite for ProjectManager Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ProjectmanagerAgent()
        assert agent.agent_id == "agent_812"
        assert agent.role == "ProjectManager Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ProjectmanagerAgent()
        result = agent.execute("test task")
        assert "ProjectManager Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ProjectmanagerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ProjectmanagerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_812"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert projectmanager_agent.agent_id == "agent_812"


class TestProjectmanagerIntegration:
    """Integration tests for ProjectManager Agent"""

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