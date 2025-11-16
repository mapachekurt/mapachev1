"""
Tests for Apollo.io Agent
"""

import pytest
from agents.saas_agents.apollo.agent import ApolloAgent, apollo_agent


class TestApolloAgent:
    """Test suite for Apollo.io Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ApolloAgent()
        assert agent.agent_id == "agent_617"
        assert agent.role == "Apollo.io Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ApolloAgent()
        result = agent.execute("test task")
        assert "Apollo.io Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ApolloAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ApolloAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_617"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert apollo_agent.agent_id == "agent_617"


class TestApolloIntegration:
    """Integration tests for Apollo.io Agent"""

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