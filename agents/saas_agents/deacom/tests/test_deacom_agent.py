"""
Tests for DEACOM ERP Agent
"""

import pytest
from agents.saas_agents.deacom.agent import DeacomAgent, deacom_agent


class TestDeacomAgent:
    """Test suite for DEACOM ERP Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DeacomAgent()
        assert agent.agent_id == "agent_1301"
        assert agent.role == "DEACOM ERP Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "manufacturing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DeacomAgent()
        result = agent.execute("test task")
        assert "DEACOM ERP Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DeacomAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DeacomAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1301"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "manufacturing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert deacom_agent.agent_id == "agent_1301"


class TestDeacomIntegration:
    """Integration tests for DEACOM ERP Agent"""

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