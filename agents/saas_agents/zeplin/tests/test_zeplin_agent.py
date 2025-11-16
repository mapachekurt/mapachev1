"""
Tests for Zeplin Agent
"""

import pytest
from agents.saas_agents.zeplin.agent import ZeplinAgent, zeplin_agent


class TestZeplinAgent:
    """Test suite for Zeplin Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZeplinAgent()
        assert agent.agent_id == "agent_761"
        assert agent.role == "Zeplin Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZeplinAgent()
        result = agent.execute("test task")
        assert "Zeplin Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZeplinAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZeplinAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_761"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zeplin_agent.agent_id == "agent_761"


class TestZeplinIntegration:
    """Integration tests for Zeplin Agent"""

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