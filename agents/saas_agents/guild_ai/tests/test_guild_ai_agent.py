"""
Tests for Guild AI Agent
"""

import pytest
from agents.saas_agents.guild_ai.agent import GuildAiAgent, guild_ai_agent


class TestGuildAiAgent:
    """Test suite for Guild AI Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GuildAiAgent()
        assert agent.agent_id == "agent_1420"
        assert agent.role == "Guild AI Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GuildAiAgent()
        result = agent.execute("test task")
        assert "Guild AI Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GuildAiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GuildAiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1420"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert guild_ai_agent.agent_id == "agent_1420"


class TestGuildAiIntegration:
    """Integration tests for Guild AI Agent"""

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