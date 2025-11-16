"""
Tests for Wrike Agent
"""

import pytest
from agents.saas_agents.wrike.agent import WrikeAgent, wrike_agent


class TestWrikeAgent:
    """Test suite for Wrike Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WrikeAgent()
        assert agent.agent_id == "agent_804"
        assert agent.role == "Wrike Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WrikeAgent()
        result = agent.execute("test task")
        assert "Wrike Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WrikeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WrikeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_804"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wrike_agent.agent_id == "agent_804"


class TestWrikeIntegration:
    """Integration tests for Wrike Agent"""

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