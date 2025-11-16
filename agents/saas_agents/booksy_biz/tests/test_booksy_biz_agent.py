"""
Tests for Booksy Biz Agent
"""

import pytest
from agents.saas_agents.booksy_biz.agent import BooksyBizAgent, booksy_biz_agent


class TestBooksyBizAgent:
    """Test suite for Booksy Biz Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BooksyBizAgent()
        assert agent.agent_id == "agent_1201"
        assert agent.role == "Booksy Biz Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BooksyBizAgent()
        result = agent.execute("test task")
        assert "Booksy Biz Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BooksyBizAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BooksyBizAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1201"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert booksy_biz_agent.agent_id == "agent_1201"


class TestBooksyBizIntegration:
    """Integration tests for Booksy Biz Agent"""

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