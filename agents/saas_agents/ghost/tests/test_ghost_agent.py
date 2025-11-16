"""
Tests for Ghost Agent
"""

import pytest
from agents.saas_agents.ghost.agent import GhostAgent, ghost_agent


class TestGhostAgent:
    """Test suite for Ghost Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GhostAgent()
        assert agent.agent_id == "agent_605"
        assert agent.role == "Ghost Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "content_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GhostAgent()
        result = agent.execute("test task")
        assert "Ghost Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GhostAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GhostAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_605"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "content_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ghost_agent.agent_id == "agent_605"


class TestGhostIntegration:
    """Integration tests for Ghost Agent"""

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