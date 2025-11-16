"""
Tests for Yandex Agent
"""

import pytest
from agents.saas_agents.yandex.agent import YandexAgent, yandex_agent


class TestYandexAgent:
    """Test suite for Yandex Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = YandexAgent()
        assert agent.agent_id == "agent_1488"
        assert agent.role == "Yandex Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = YandexAgent()
        result = agent.execute("test task")
        assert "Yandex Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = YandexAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = YandexAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1488"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert yandex_agent.agent_id == "agent_1488"


class TestYandexIntegration:
    """Integration tests for Yandex Agent"""

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