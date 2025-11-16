"""
Tests for LINE Agent
"""

import pytest
from agents.saas_agents.line.agent import LineAgent, line_agent


class TestLineAgent:
    """Test suite for LINE Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LineAgent()
        assert agent.agent_id == "agent_836"
        assert agent.role == "LINE Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LineAgent()
        result = agent.execute("test task")
        assert "LINE Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LineAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LineAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_836"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert line_agent.agent_id == "agent_836"


class TestLineIntegration:
    """Integration tests for LINE Agent"""

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