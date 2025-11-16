"""
Tests for iXact Contact Agent
"""

import pytest
from agents.saas_agents.ixact_contact.agent import IxactContactAgent, ixact_contact_agent


class TestIxactContactAgent:
    """Test suite for iXact Contact Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = IxactContactAgent()
        assert agent.agent_id == "agent_1083"
        assert agent.role == "iXact Contact Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = IxactContactAgent()
        result = agent.execute("test task")
        assert "iXact Contact Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = IxactContactAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = IxactContactAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1083"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ixact_contact_agent.agent_id == "agent_1083"


class TestIxactContactIntegration:
    """Integration tests for iXact Contact Agent"""

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