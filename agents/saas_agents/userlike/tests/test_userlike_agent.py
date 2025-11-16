"""
Tests for Userlike Agent
"""

import pytest
from agents.saas_agents.userlike.agent import UserlikeAgent, userlike_agent


class TestUserlikeAgent:
    """Test suite for Userlike Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = UserlikeAgent()
        assert agent.agent_id == "agent_1000"
        assert agent.role == "Userlike Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = UserlikeAgent()
        result = agent.execute("test task")
        assert "Userlike Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = UserlikeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = UserlikeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1000"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert userlike_agent.agent_id == "agent_1000"


class TestUserlikeIntegration:
    """Integration tests for Userlike Agent"""

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