"""
Tests for Insomnia Agent
"""

import pytest
from agents.saas_agents.insomnia.agent import InsomniaAgent, insomnia_agent


class TestInsomniaAgent:
    """Test suite for Insomnia Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = InsomniaAgent()
        assert agent.agent_id == "agent_711"
        assert agent.role == "Insomnia Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "api"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = InsomniaAgent()
        result = agent.execute("test task")
        assert "Insomnia Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = InsomniaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = InsomniaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_711"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "api"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert insomnia_agent.agent_id == "agent_711"


class TestInsomniaIntegration:
    """Integration tests for Insomnia Agent"""

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