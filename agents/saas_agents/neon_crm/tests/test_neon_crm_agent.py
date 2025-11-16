"""
Tests for Neon CRM Agent
"""

import pytest
from agents.saas_agents.neon_crm.agent import NeonCrmAgent, neon_crm_agent


class TestNeonCrmAgent:
    """Test suite for Neon CRM Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NeonCrmAgent()
        assert agent.agent_id == "agent_1255"
        assert agent.role == "Neon CRM Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "nonprofit"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NeonCrmAgent()
        result = agent.execute("test task")
        assert "Neon CRM Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NeonCrmAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NeonCrmAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1255"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "nonprofit"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert neon_crm_agent.agent_id == "agent_1255"


class TestNeonCrmIntegration:
    """Integration tests for Neon CRM Agent"""

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