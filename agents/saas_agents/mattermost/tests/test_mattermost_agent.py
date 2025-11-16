"""
Tests for Mattermost Agent
"""

import pytest
from agents.saas_agents.mattermost.agent import MattermostAgent, mattermost_agent


class TestMattermostAgent:
    """Test suite for Mattermost Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MattermostAgent()
        assert agent.agent_id == "agent_839"
        assert agent.role == "Mattermost Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MattermostAgent()
        result = agent.execute("test task")
        assert "Mattermost Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MattermostAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MattermostAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_839"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mattermost_agent.agent_id == "agent_839"


class TestMattermostIntegration:
    """Integration tests for Mattermost Agent"""

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