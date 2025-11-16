"""
Tests for Authorize.net Agent
"""

import pytest
from agents.saas_agents.authorize_net.agent import AuthorizeNetAgent, authorize_net_agent


class TestAuthorizeNetAgent:
    """Test suite for Authorize.net Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AuthorizeNetAgent()
        assert agent.agent_id == "agent_924"
        assert agent.role == "Authorize.net Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AuthorizeNetAgent()
        result = agent.execute("test task")
        assert "Authorize.net Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AuthorizeNetAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AuthorizeNetAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_924"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert authorize_net_agent.agent_id == "agent_924"


class TestAuthorizeNetIntegration:
    """Integration tests for Authorize.net Agent"""

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