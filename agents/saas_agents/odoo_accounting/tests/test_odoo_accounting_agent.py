"""
Tests for Odoo Accounting Agent
"""

import pytest
from agents.saas_agents.odoo_accounting.agent import OdooAccountingAgent, odoo_accounting_agent


class TestOdooAccountingAgent:
    """Test suite for Odoo Accounting Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OdooAccountingAgent()
        assert agent.agent_id == "agent_905"
        assert agent.role == "Odoo Accounting Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OdooAccountingAgent()
        result = agent.execute("test task")
        assert "Odoo Accounting Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OdooAccountingAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OdooAccountingAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_905"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert odoo_accounting_agent.agent_id == "agent_905"


class TestOdooAccountingIntegration:
    """Integration tests for Odoo Accounting Agent"""

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