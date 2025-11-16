"""
Tests for Telegram Agent
"""

import pytest
from agents.saas_agents.telegram.agent import TelegramAgent, telegram_agent


class TestTelegramAgent:
    """Test suite for Telegram Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TelegramAgent()
        assert agent.agent_id == "agent_832"
        assert agent.role == "Telegram Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TelegramAgent()
        result = agent.execute("test task")
        assert "Telegram Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TelegramAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TelegramAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_832"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert telegram_agent.agent_id == "agent_832"


class TestTelegramIntegration:
    """Integration tests for Telegram Agent"""

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