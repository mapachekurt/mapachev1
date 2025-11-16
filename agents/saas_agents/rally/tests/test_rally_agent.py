"""
Tests for Rally Agent
"""

import pytest
from agents.saas_agents.rally.agent import RallyAgent, rally_agent


class TestRallyAgent:
    """Test suite for Rally Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RallyAgent()
        assert agent.agent_id == "agent_861"
        assert agent.role == "Rally Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RallyAgent()
        result = agent.execute("test task")
        assert "Rally Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RallyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RallyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_861"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rally_agent.agent_id == "agent_861"


class TestRallyIntegration:
    """Integration tests for Rally Agent"""

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