"""
Tests for Zapier Agent
"""

import pytest
from agents.saas_agents.zapier.agent import ZapierAgent, zapier_agent


class TestZapierAgent:
    """Test suite for Zapier Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZapierAgent()
        assert agent.agent_id == "agent_1328"
        assert agent.role == "Zapier Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZapierAgent()
        result = agent.execute("test task")
        assert "Zapier Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZapierAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZapierAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1328"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zapier_agent.agent_id == "agent_1328"


class TestZapierIntegration:
    """Integration tests for Zapier Agent"""

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