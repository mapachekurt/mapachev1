"""
Tests for Mercado Libre Agent
"""

import pytest
from agents.saas_agents.mercado_libre.agent import MercadoLibreAgent, mercado_libre_agent


class TestMercadoLibreAgent:
    """Test suite for Mercado Libre Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MercadoLibreAgent()
        assert agent.agent_id == "agent_1477"
        assert agent.role == "Mercado Libre Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MercadoLibreAgent()
        result = agent.execute("test task")
        assert "Mercado Libre Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MercadoLibreAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MercadoLibreAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1477"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mercado_libre_agent.agent_id == "agent_1477"


class TestMercadoLibreIntegration:
    """Integration tests for Mercado Libre Agent"""

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