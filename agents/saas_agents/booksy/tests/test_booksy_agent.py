"""
Tests for Booksy Agent
"""

import pytest
from agents.saas_agents.booksy.agent import BooksyAgent, booksy_agent


class TestBooksyAgent:
    """Test suite for Booksy Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BooksyAgent()
        assert agent.agent_id == "agent_854"
        assert agent.role == "Booksy Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BooksyAgent()
        result = agent.execute("test task")
        assert "Booksy Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BooksyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BooksyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_854"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert booksy_agent.agent_id == "agent_854"


class TestBooksyIntegration:
    """Integration tests for Booksy Agent"""

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