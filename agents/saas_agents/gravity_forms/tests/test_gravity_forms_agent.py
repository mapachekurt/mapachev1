"""
Tests for Gravity Forms Agent
"""

import pytest
from agents.saas_agents.gravity_forms.agent import GravityFormsAgent, gravity_forms_agent


class TestGravityFormsAgent:
    """Test suite for Gravity Forms Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GravityFormsAgent()
        assert agent.agent_id == "agent_887"
        assert agent.role == "Gravity Forms Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GravityFormsAgent()
        result = agent.execute("test task")
        assert "Gravity Forms Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GravityFormsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GravityFormsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_887"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gravity_forms_agent.agent_id == "agent_887"


class TestGravityFormsIntegration:
    """Integration tests for Gravity Forms Agent"""

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