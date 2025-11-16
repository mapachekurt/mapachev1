"""
Tests for 6Connex Agent
"""

import pytest
from agents.saas_agents.6connex.agent import 6connexAgent, 6connex_agent


class Test6connexAgent:
    """Test suite for 6Connex Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = 6connexAgent()
        assert agent.agent_id == "agent_1229"
        assert agent.role == "6Connex Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = 6connexAgent()
        result = agent.execute("test task")
        assert "6Connex Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = 6connexAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = 6connexAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1229"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert 6connex_agent.agent_id == "agent_1229"


class Test6connexIntegration:
    """Integration tests for 6Connex Agent"""

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