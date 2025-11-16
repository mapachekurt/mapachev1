"""
Tests for Basecamp Agent
"""

import pytest
from agents.saas_agents.basecamp.agent import BasecampAgent, basecamp_agent


class TestBasecampAgent:
    """Test suite for Basecamp Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BasecampAgent()
        assert agent.agent_id == "agent_803"
        assert agent.role == "Basecamp Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BasecampAgent()
        result = agent.execute("test task")
        assert "Basecamp Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BasecampAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BasecampAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_803"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert basecamp_agent.agent_id == "agent_803"


class TestBasecampIntegration:
    """Integration tests for Basecamp Agent"""

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