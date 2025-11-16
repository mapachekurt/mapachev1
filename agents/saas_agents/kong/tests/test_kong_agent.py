"""
Tests for Kong Agent
"""

import pytest
from agents.saas_agents.kong.agent import KongAgent, kong_agent


class TestKongAgent:
    """Test suite for Kong Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KongAgent()
        assert agent.agent_id == "agent_704"
        assert agent.role == "Kong Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "api"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KongAgent()
        result = agent.execute("test task")
        assert "Kong Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KongAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KongAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_704"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "api"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kong_agent.agent_id == "agent_704"


class TestKongIntegration:
    """Integration tests for Kong Agent"""

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