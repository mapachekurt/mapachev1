"""
Tests for Ecwid Agent
"""

import pytest
from agents.saas_agents.ecwid.agent import EcwidAgent, ecwid_agent


class TestEcwidAgent:
    """Test suite for Ecwid Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = EcwidAgent()
        assert agent.agent_id == "agent_972"
        assert agent.role == "Ecwid Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = EcwidAgent()
        result = agent.execute("test task")
        assert "Ecwid Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = EcwidAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = EcwidAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_972"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ecwid_agent.agent_id == "agent_972"


class TestEcwidIntegration:
    """Integration tests for Ecwid Agent"""

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