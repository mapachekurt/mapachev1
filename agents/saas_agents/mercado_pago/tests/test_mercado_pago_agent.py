"""
Tests for Mercado Pago Agent
"""

import pytest
from agents.saas_agents.mercado_pago.agent import MercadoPagoAgent, mercado_pago_agent


class TestMercadoPagoAgent:
    """Test suite for Mercado Pago Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MercadoPagoAgent()
        assert agent.agent_id == "agent_1478"
        assert agent.role == "Mercado Pago Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MercadoPagoAgent()
        result = agent.execute("test task")
        assert "Mercado Pago Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MercadoPagoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MercadoPagoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1478"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mercado_pago_agent.agent_id == "agent_1478"


class TestMercadoPagoIntegration:
    """Integration tests for Mercado Pago Agent"""

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