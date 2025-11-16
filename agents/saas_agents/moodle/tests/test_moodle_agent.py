"""
Tests for Moodle Agent
"""

import pytest
from agents.saas_agents.moodle.agent import MoodleAgent, moodle_agent


class TestMoodleAgent:
    """Test suite for Moodle Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MoodleAgent()
        assert agent.agent_id == "agent_1053"
        assert agent.role == "Moodle Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MoodleAgent()
        result = agent.execute("test task")
        assert "Moodle Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MoodleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MoodleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1053"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert moodle_agent.agent_id == "agent_1053"


class TestMoodleIntegration:
    """Integration tests for Moodle Agent"""

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