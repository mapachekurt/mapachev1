"""
Tests for Justworks Agent
"""

import pytest
from agents.saas_agents.justworks.agent import JustworksAgent, justworks_agent


class TestJustworksAgent:
    """Test suite for Justworks Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JustworksAgent()
        assert agent.agent_id == "agent_959"
        assert agent.role == "Justworks Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JustworksAgent()
        result = agent.execute("test task")
        assert "Justworks Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JustworksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JustworksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_959"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert justworks_agent.agent_id == "agent_959"


class TestJustworksIntegration:
    """Integration tests for Justworks Agent"""

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