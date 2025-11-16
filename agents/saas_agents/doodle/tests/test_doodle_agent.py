"""
Tests for Doodle Agent
"""

import pytest
from agents.saas_agents.doodle.agent import DoodleAgent, doodle_agent


class TestDoodleAgent:
    """Test suite for Doodle Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DoodleAgent()
        assert agent.agent_id == "agent_849"
        assert agent.role == "Doodle Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DoodleAgent()
        result = agent.execute("test task")
        assert "Doodle Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DoodleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DoodleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_849"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert doodle_agent.agent_id == "agent_849"


class TestDoodleIntegration:
    """Integration tests for Doodle Agent"""

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