"""
Tests for Zoho Books Agent
"""

import pytest
from agents.saas_agents.zoho_books.agent import ZohoBooksAgent, zoho_books_agent


class TestZohoBooksAgent:
    """Test suite for Zoho Books Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZohoBooksAgent()
        assert agent.agent_id == "agent_895"
        assert agent.role == "Zoho Books Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZohoBooksAgent()
        result = agent.execute("test task")
        assert "Zoho Books Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZohoBooksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZohoBooksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_895"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zoho_books_agent.agent_id == "agent_895"


class TestZohoBooksIntegration:
    """Integration tests for Zoho Books Agent"""

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