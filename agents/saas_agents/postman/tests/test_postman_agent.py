"""
Tests for Postman Agent
"""

import pytest
from agents.saas_agents.postman.agent import PostmanAgent, postman_agent


class TestPostmanAgent:
    """Test suite for Postman Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PostmanAgent()
        assert agent.agent_id == "agent_702"
        assert agent.role == "Postman Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "api"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PostmanAgent()
        result = agent.execute("test task")
        assert "Postman Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PostmanAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PostmanAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_702"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "api"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert postman_agent.agent_id == "agent_702"


class TestPostmanIntegration:
    """Integration tests for Postman Agent"""

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