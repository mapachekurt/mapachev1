"""
Tests for Hootsuite Agent
"""

import pytest
from agents.saas_agents.hootsuite.agent import HootsuiteAgent, hootsuite_agent


class TestHootsuiteAgent:
    """Test suite for Hootsuite Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HootsuiteAgent()
        assert agent.agent_id == "agent_542"
        assert agent.role == "Hootsuite Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "social_media"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HootsuiteAgent()
        result = agent.execute("test task")
        assert "Hootsuite Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HootsuiteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HootsuiteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_542"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "social_media"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hootsuite_agent.agent_id == "agent_542"


class TestHootsuiteIntegration:
    """Integration tests for Hootsuite Agent"""

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