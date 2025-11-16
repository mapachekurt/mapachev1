"""
Tests for Agile CRM Agent
"""

import pytest
from agents.saas_agents.agile_crm.agent import AgileCrmAgent, agile_crm_agent


class TestAgileCrmAgent:
    """Test suite for Agile CRM Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AgileCrmAgent()
        assert agent.agent_id == "agent_578"
        assert agent.role == "Agile CRM Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AgileCrmAgent()
        result = agent.execute("test task")
        assert "Agile CRM Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AgileCrmAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AgileCrmAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_578"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert agile_crm_agent.agent_id == "agent_578"


class TestAgileCrmIntegration:
    """Integration tests for Agile CRM Agent"""

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