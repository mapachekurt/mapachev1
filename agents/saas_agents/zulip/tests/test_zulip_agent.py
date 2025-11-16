"""
Tests for Zulip Agent
"""

import pytest
from agents.saas_agents.zulip.agent import ZulipAgent, zulip_agent


class TestZulipAgent:
    """Test suite for Zulip Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZulipAgent()
        assert agent.agent_id == "agent_840"
        assert agent.role == "Zulip Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZulipAgent()
        result = agent.execute("test task")
        assert "Zulip Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZulipAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZulipAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_840"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zulip_agent.agent_id == "agent_840"


class TestZulipIntegration:
    """Integration tests for Zulip Agent"""

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