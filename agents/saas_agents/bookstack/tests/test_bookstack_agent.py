"""
Tests for BookStack Agent
"""

import pytest
from agents.saas_agents.bookstack.agent import BookstackAgent, bookstack_agent


class TestBookstackAgent:
    """Test suite for BookStack Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BookstackAgent()
        assert agent.agent_id == "agent_778"
        assert agent.role == "BookStack Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BookstackAgent()
        result = agent.execute("test task")
        assert "BookStack Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BookstackAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BookstackAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_778"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bookstack_agent.agent_id == "agent_778"


class TestBookstackIntegration:
    """Integration tests for BookStack Agent"""

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