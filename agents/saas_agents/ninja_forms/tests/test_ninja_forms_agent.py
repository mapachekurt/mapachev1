"""
Tests for Ninja Forms Agent
"""

import pytest
from agents.saas_agents.ninja_forms.agent import NinjaFormsAgent, ninja_forms_agent


class TestNinjaFormsAgent:
    """Test suite for Ninja Forms Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NinjaFormsAgent()
        assert agent.agent_id == "agent_888"
        assert agent.role == "Ninja Forms Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NinjaFormsAgent()
        result = agent.execute("test task")
        assert "Ninja Forms Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NinjaFormsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NinjaFormsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_888"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ninja_forms_agent.agent_id == "agent_888"


class TestNinjaFormsIntegration:
    """Integration tests for Ninja Forms Agent"""

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