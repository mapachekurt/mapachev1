"""
Tests for Wise (TransferWise) Agent
"""

import pytest
from agents.saas_agents.transferwise.agent import TransferwiseAgent, transferwise_agent


class TestTransferwiseAgent:
    """Test suite for Wise (TransferWise) Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TransferwiseAgent()
        assert agent.agent_id == "agent_935"
        assert agent.role == "Wise (TransferWise) Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TransferwiseAgent()
        result = agent.execute("test task")
        assert "Wise (TransferWise) Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TransferwiseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TransferwiseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_935"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert transferwise_agent.agent_id == "agent_935"


class TestTransferwiseIntegration:
    """Integration tests for Wise (TransferWise) Agent"""

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