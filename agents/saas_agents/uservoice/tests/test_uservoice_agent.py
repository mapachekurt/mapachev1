"""
Tests for UserVoice Agent
"""

import pytest
from agents.saas_agents.uservoice.agent import UservoiceAgent, uservoice_agent


class TestUservoiceAgent:
    """Test suite for UserVoice Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = UservoiceAgent()
        assert agent.agent_id == "agent_992"
        assert agent.role == "UserVoice Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = UservoiceAgent()
        result = agent.execute("test task")
        assert "UserVoice Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = UservoiceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = UservoiceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_992"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert uservoice_agent.agent_id == "agent_992"


class TestUservoiceIntegration:
    """Integration tests for UserVoice Agent"""

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