"""
Tests for Hasura Agent
"""

import pytest
from agents.saas_agents.hasura.agent import HasuraAgent, hasura_agent


class TestHasuraAgent:
    """Test suite for Hasura Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HasuraAgent()
        assert agent.agent_id == "agent_710"
        assert agent.role == "Hasura Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "api"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HasuraAgent()
        result = agent.execute("test task")
        assert "Hasura Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HasuraAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HasuraAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_710"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "api"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hasura_agent.agent_id == "agent_710"


class TestHasuraIntegration:
    """Integration tests for Hasura Agent"""

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