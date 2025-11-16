"""
Tests for Freshsales Agent
"""

import pytest
from agents.saas_agents.freshsales.agent import FreshsalesAgent, freshsales_agent


class TestFreshsalesAgent:
    """Test suite for Freshsales Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FreshsalesAgent()
        assert agent.agent_id == "agent_574"
        assert agent.role == "Freshsales Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FreshsalesAgent()
        result = agent.execute("test task")
        assert "Freshsales Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FreshsalesAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FreshsalesAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_574"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert freshsales_agent.agent_id == "agent_574"


class TestFreshsalesIntegration:
    """Integration tests for Freshsales Agent"""

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