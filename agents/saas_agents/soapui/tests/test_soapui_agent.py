"""
Tests for SoapUI Agent
"""

import pytest
from agents.saas_agents.soapui.agent import SoapuiAgent, soapui_agent


class TestSoapuiAgent:
    """Test suite for SoapUI Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SoapuiAgent()
        assert agent.agent_id == "agent_1393"
        assert agent.role == "SoapUI Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SoapuiAgent()
        result = agent.execute("test task")
        assert "SoapUI Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SoapuiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SoapuiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1393"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert soapui_agent.agent_id == "agent_1393"


class TestSoapuiIntegration:
    """Integration tests for SoapUI Agent"""

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