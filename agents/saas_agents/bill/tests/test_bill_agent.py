"""
Tests for Bill.com Agent
"""

import pytest
from agents.saas_agents.bill.agent import BillAgent, bill_agent


class TestBillAgent:
    """Test suite for Bill.com Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BillAgent()
        assert agent.agent_id == "agent_909"
        assert agent.role == "Bill.com Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BillAgent()
        result = agent.execute("test task")
        assert "Bill.com Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BillAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BillAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_909"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bill_agent.agent_id == "agent_909"


class TestBillIntegration:
    """Integration tests for Bill.com Agent"""

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