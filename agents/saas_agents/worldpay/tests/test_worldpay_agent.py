"""
Tests for Worldpay Agent
"""

import pytest
from agents.saas_agents.worldpay.agent import WorldpayAgent, worldpay_agent


class TestWorldpayAgent:
    """Test suite for Worldpay Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WorldpayAgent()
        assert agent.agent_id == "agent_925"
        assert agent.role == "Worldpay Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WorldpayAgent()
        result = agent.execute("test task")
        assert "Worldpay Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WorldpayAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WorldpayAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_925"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert worldpay_agent.agent_id == "agent_925"


class TestWorldpayIntegration:
    """Integration tests for Worldpay Agent"""

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