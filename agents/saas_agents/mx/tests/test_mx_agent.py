"""
Tests for MX Agent
"""

import pytest
from agents.saas_agents.mx.agent import MxAgent, mx_agent


class TestMxAgent:
    """Test suite for MX Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MxAgent()
        assert agent.agent_id == "agent_1505"
        assert agent.role == "MX Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MxAgent()
        result = agent.execute("test task")
        assert "MX Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MxAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MxAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1505"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mx_agent.agent_id == "agent_1505"


class TestMxIntegration:
    """Integration tests for MX Agent"""

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