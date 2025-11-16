"""
Tests for RudderStack Agent
"""

import pytest
from agents.saas_agents.rudderstack.agent import RudderstackAgent, rudderstack_agent


class TestRudderstackAgent:
    """Test suite for RudderStack Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RudderstackAgent()
        assert agent.agent_id == "agent_1388"
        assert agent.role == "RudderStack Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "data"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RudderstackAgent()
        result = agent.execute("test task")
        assert "RudderStack Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RudderstackAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RudderstackAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1388"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "data"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rudderstack_agent.agent_id == "agent_1388"


class TestRudderstackIntegration:
    """Integration tests for RudderStack Agent"""

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