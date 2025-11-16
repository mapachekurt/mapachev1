"""
Tests for Braintree Agent
"""

import pytest
from agents.saas_agents.braintree.agent import BraintreeAgent, braintree_agent


class TestBraintreeAgent:
    """Test suite for Braintree Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BraintreeAgent()
        assert agent.agent_id == "agent_923"
        assert agent.role == "Braintree Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BraintreeAgent()
        result = agent.execute("test task")
        assert "Braintree Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BraintreeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BraintreeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_923"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert braintree_agent.agent_id == "agent_923"


class TestBraintreeIntegration:
    """Integration tests for Braintree Agent"""

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