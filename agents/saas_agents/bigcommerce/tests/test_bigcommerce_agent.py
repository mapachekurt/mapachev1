"""
Tests for BigCommerce Agent
"""

import pytest
from agents.saas_agents.bigcommerce.agent import BigcommerceAgent, bigcommerce_agent


class TestBigcommerceAgent:
    """Test suite for BigCommerce Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BigcommerceAgent()
        assert agent.agent_id == "agent_968"
        assert agent.role == "BigCommerce Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BigcommerceAgent()
        result = agent.execute("test task")
        assert "BigCommerce Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BigcommerceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BigcommerceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_968"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bigcommerce_agent.agent_id == "agent_968"


class TestBigcommerceIntegration:
    """Integration tests for BigCommerce Agent"""

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