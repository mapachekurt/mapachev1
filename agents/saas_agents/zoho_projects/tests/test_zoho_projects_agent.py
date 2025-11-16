"""
Tests for Zoho Projects Agent
"""

import pytest
from agents.saas_agents.zoho_projects.agent import ZohoProjectsAgent, zoho_projects_agent


class TestZohoProjectsAgent:
    """Test suite for Zoho Projects Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZohoProjectsAgent()
        assert agent.agent_id == "agent_815"
        assert agent.role == "Zoho Projects Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZohoProjectsAgent()
        result = agent.execute("test task")
        assert "Zoho Projects Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZohoProjectsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZohoProjectsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_815"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zoho_projects_agent.agent_id == "agent_815"


class TestZohoProjectsIntegration:
    """Integration tests for Zoho Projects Agent"""

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