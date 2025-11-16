"""
Tests for OpenTable Agent
"""

import pytest
from agents.saas_agents.opentable.agent import OpentableAgent, opentable_agent


class TestOpentableAgent:
    """Test suite for OpenTable Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OpentableAgent()
        assert agent.agent_id == "agent_1192"
        assert agent.role == "OpenTable Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OpentableAgent()
        result = agent.execute("test task")
        assert "OpenTable Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OpentableAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OpentableAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1192"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert opentable_agent.agent_id == "agent_1192"


class TestOpentableIntegration:
    """Integration tests for OpenTable Agent"""

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