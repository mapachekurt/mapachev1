"""
Tests for Books by Zoho Agent
"""

import pytest
from agents.saas_agents.books.agent import BooksAgent, books_agent


class TestBooksAgent:
    """Test suite for Books by Zoho Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BooksAgent()
        assert agent.agent_id == "agent_901"
        assert agent.role == "Books by Zoho Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BooksAgent()
        result = agent.execute("test task")
        assert "Books by Zoho Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BooksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BooksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_901"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert books_agent.agent_id == "agent_901"


class TestBooksIntegration:
    """Integration tests for Books by Zoho Agent"""

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