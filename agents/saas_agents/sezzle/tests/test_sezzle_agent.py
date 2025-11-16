"""
Tests for Sezzle Agent
"""

import pytest
from agents.saas_agents.sezzle.agent import SezzleAgent, sezzle_agent


class TestSezzleAgent:
    """Test suite for Sezzle Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SezzleAgent()
        assert agent.agent_id == "agent_933"
        assert agent.role == "Sezzle Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SezzleAgent()
        result = agent.execute("test task")
        assert "Sezzle Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SezzleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SezzleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_933"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sezzle_agent.agent_id == "agent_933"


class TestSezzleIntegration:
    """Integration tests for Sezzle Agent"""

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