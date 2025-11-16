"""
Tests for WooCommerce Agent
"""

import pytest
from agents.saas_agents.woocommerce.agent import WoocommerceAgent, woocommerce_agent


class TestWoocommerceAgent:
    """Test suite for WooCommerce Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WoocommerceAgent()
        assert agent.agent_id == "agent_967"
        assert agent.role == "WooCommerce Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WoocommerceAgent()
        result = agent.execute("test task")
        assert "WooCommerce Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WoocommerceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WoocommerceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_967"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert woocommerce_agent.agent_id == "agent_967"


class TestWoocommerceIntegration:
    """Integration tests for WooCommerce Agent"""

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