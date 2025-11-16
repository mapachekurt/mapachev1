"""
Tests for Act-On Agent
"""

import pytest
from agents.saas_agents.act_on.agent import ActOnAgent, act_on_agent


class TestActOnAgent:
    """Test suite for Act-On Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ActOnAgent()
        assert agent.agent_id == "agent_586"
        assert agent.role == "Act-On Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "marketing_automation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ActOnAgent()
        result = agent.execute("test task")
        assert "Act-On Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ActOnAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ActOnAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_586"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "marketing_automation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert act_on_agent.agent_id == "agent_586"


class TestActOnIntegration:
    """Integration tests for Act-On Agent"""

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