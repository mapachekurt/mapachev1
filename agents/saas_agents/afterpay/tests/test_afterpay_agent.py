"""
Tests for Afterpay Agent
"""

import pytest
from agents.saas_agents.afterpay.agent import AfterpayAgent, afterpay_agent


class TestAfterpayAgent:
    """Test suite for Afterpay Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AfterpayAgent()
        assert agent.agent_id == "agent_931"
        assert agent.role == "Afterpay Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AfterpayAgent()
        result = agent.execute("test task")
        assert "Afterpay Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AfterpayAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AfterpayAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_931"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert afterpay_agent.agent_id == "agent_931"


class TestAfterpayIntegration:
    """Integration tests for Afterpay Agent"""

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