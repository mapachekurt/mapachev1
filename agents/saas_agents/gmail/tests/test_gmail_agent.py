"""
Tests for Gmail Agent
"""

import pytest
from agents.saas_agents.gmail.agent import GmailAgent, gmail_agent


class TestGmailAgent:
    """Test suite for Gmail Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GmailAgent()
        assert agent.agent_id == "agent_516"
        assert agent.role == "Gmail Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "email"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GmailAgent()
        result = agent.execute("test task")
        assert "Gmail Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GmailAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GmailAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_516"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "email"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gmail_agent.agent_id == "agent_516"


class TestGmailIntegration:
    """Integration tests for Gmail Agent"""

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