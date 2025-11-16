"""
Tests for Aventri Agent
"""

import pytest
from agents.saas_agents.aventri.agent import AventriAgent, aventri_agent


class TestAventriAgent:
    """Test suite for Aventri Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AventriAgent()
        assert agent.agent_id == "agent_1221"
        assert agent.role == "Aventri Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AventriAgent()
        result = agent.execute("test task")
        assert "Aventri Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AventriAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AventriAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1221"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aventri_agent.agent_id == "agent_1221"


class TestAventriIntegration:
    """Integration tests for Aventri Agent"""

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