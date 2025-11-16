"""
Tests for Constant Contact Agent
"""

import pytest
from agents.saas_agents.constant_contact.agent import ConstantContactAgent, constant_contact_agent


class TestConstantContactAgent:
    """Test suite for Constant Contact Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ConstantContactAgent()
        assert agent.agent_id == "agent_533"
        assert agent.role == "Constant Contact Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ConstantContactAgent()
        result = agent.execute("test task")
        assert "Constant Contact Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ConstantContactAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ConstantContactAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_533"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert constant_contact_agent.agent_id == "agent_533"


class TestConstantContactIntegration:
    """Integration tests for Constant Contact Agent"""

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