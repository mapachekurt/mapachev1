"""
Tests for Nutshell Agent
"""

import pytest
from agents.saas_agents.nutshell.agent import NutshellAgent, nutshell_agent


class TestNutshellAgent:
    """Test suite for Nutshell Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NutshellAgent()
        assert agent.agent_id == "agent_581"
        assert agent.role == "Nutshell Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NutshellAgent()
        result = agent.execute("test task")
        assert "Nutshell Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NutshellAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NutshellAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_581"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nutshell_agent.agent_id == "agent_581"


class TestNutshellIntegration:
    """Integration tests for Nutshell Agent"""

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