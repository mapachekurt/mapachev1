"""
Tests for Customer.io Agent
"""

import pytest
from agents.saas_agents.customer_io.agent import CustomerIoAgent, customer_io_agent


class TestCustomerIoAgent:
    """Test suite for Customer.io Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CustomerIoAgent()
        assert agent.agent_id == "agent_588"
        assert agent.role == "Customer.io Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "marketing_automation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CustomerIoAgent()
        result = agent.execute("test task")
        assert "Customer.io Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CustomerIoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CustomerIoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_588"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "marketing_automation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert customer_io_agent.agent_id == "agent_588"


class TestCustomerIoIntegration:
    """Integration tests for Customer.io Agent"""

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