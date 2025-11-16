"""
Tests for REST Assured Agent
"""

import pytest
from agents.saas_agents.rest_assured.agent import RestAssuredAgent, rest_assured_agent


class TestRestAssuredAgent:
    """Test suite for REST Assured Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RestAssuredAgent()
        assert agent.agent_id == "agent_1394"
        assert agent.role == "REST Assured Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RestAssuredAgent()
        result = agent.execute("test task")
        assert "REST Assured Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RestAssuredAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RestAssuredAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1394"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rest_assured_agent.agent_id == "agent_1394"


class TestRestAssuredIntegration:
    """Integration tests for REST Assured Agent"""

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