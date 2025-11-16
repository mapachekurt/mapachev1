"""
Tests for Nimble Agent
"""

import pytest
from agents.saas_agents.nimble.agent import NimbleAgent, nimble_agent


class TestNimbleAgent:
    """Test suite for Nimble Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NimbleAgent()
        assert agent.agent_id == "agent_577"
        assert agent.role == "Nimble Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NimbleAgent()
        result = agent.execute("test task")
        assert "Nimble Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NimbleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NimbleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_577"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nimble_agent.agent_id == "agent_577"


class TestNimbleIntegration:
    """Integration tests for Nimble Agent"""

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