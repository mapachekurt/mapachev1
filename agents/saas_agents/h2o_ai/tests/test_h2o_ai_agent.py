"""
Tests for H2O.ai Agent
"""

import pytest
from agents.saas_agents.h2o_ai.agent import H2oAiAgent, h2o_ai_agent


class TestH2oAiAgent:
    """Test suite for H2O.ai Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = H2oAiAgent()
        assert agent.agent_id == "agent_1414"
        assert agent.role == "H2O.ai Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = H2oAiAgent()
        result = agent.execute("test task")
        assert "H2O.ai Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = H2oAiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = H2oAiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1414"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert h2o_ai_agent.agent_id == "agent_1414"


class TestH2oAiIntegration:
    """Integration tests for H2O.ai Agent"""

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