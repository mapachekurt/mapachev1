"""
Tests for Formstack Agent
"""

import pytest
from agents.saas_agents.formstack.agent import FormstackAgent, formstack_agent


class TestFormstackAgent:
    """Test suite for Formstack Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FormstackAgent()
        assert agent.agent_id == "agent_881"
        assert agent.role == "Formstack Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FormstackAgent()
        result = agent.execute("test task")
        assert "Formstack Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FormstackAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FormstackAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_881"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert formstack_agent.agent_id == "agent_881"


class TestFormstackIntegration:
    """Integration tests for Formstack Agent"""

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