"""
Tests for Checkout.com Agent
"""

import pytest
from agents.saas_agents.checkout.agent import CheckoutAgent, checkout_agent


class TestCheckoutAgent:
    """Test suite for Checkout.com Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CheckoutAgent()
        assert agent.agent_id == "agent_926"
        assert agent.role == "Checkout.com Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CheckoutAgent()
        result = agent.execute("test task")
        assert "Checkout.com Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CheckoutAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CheckoutAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_926"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert checkout_agent.agent_id == "agent_926"


class TestCheckoutIntegration:
    """Integration tests for Checkout.com Agent"""

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