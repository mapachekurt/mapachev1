"""
Tests for Teladoc Agent
"""

import pytest
from agents.saas_agents.teladoc.agent import TeladocAgent, teladoc_agent


class TestTeladocAgent:
    """Test suite for Teladoc Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TeladocAgent()
        assert agent.agent_id == "agent_1495"
        assert agent.role == "Teladoc Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TeladocAgent()
        result = agent.execute("test task")
        assert "Teladoc Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TeladocAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TeladocAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1495"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert teladoc_agent.agent_id == "agent_1495"


class TestTeladocIntegration:
    """Integration tests for Teladoc Agent"""

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