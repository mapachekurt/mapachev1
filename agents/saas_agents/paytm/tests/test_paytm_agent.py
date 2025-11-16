"""
Tests for Paytm Agent
"""

import pytest
from agents.saas_agents.paytm.agent import PaytmAgent, paytm_agent


class TestPaytmAgent:
    """Test suite for Paytm Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PaytmAgent()
        assert agent.agent_id == "agent_928"
        assert agent.role == "Paytm Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PaytmAgent()
        result = agent.execute("test task")
        assert "Paytm Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PaytmAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PaytmAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_928"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert paytm_agent.agent_id == "agent_928"


class TestPaytmIntegration:
    """Integration tests for Paytm Agent"""

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