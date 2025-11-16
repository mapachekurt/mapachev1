"""
Tests for Ping Identity Agent
"""

import pytest
from agents.saas_agents.ping_identity.agent import PingIdentityAgent, ping_identity_agent


class TestPingIdentityAgent:
    """Test suite for Ping Identity Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PingIdentityAgent()
        assert agent.agent_id == "agent_1434"
        assert agent.role == "Ping Identity Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PingIdentityAgent()
        result = agent.execute("test task")
        assert "Ping Identity Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PingIdentityAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PingIdentityAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1434"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ping_identity_agent.agent_id == "agent_1434"


class TestPingIdentityIntegration:
    """Integration tests for Ping Identity Agent"""

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