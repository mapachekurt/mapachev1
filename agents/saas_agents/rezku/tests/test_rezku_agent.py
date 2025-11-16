"""
Tests for Rezku Agent
"""

import pytest
from agents.saas_agents.rezku.agent import RezkuAgent, rezku_agent


class TestRezkuAgent:
    """Test suite for Rezku Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RezkuAgent()
        assert agent.agent_id == "agent_1167"
        assert agent.role == "Rezku Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RezkuAgent()
        result = agent.execute("test task")
        assert "Rezku Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RezkuAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RezkuAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1167"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rezku_agent.agent_id == "agent_1167"


class TestRezkuIntegration:
    """Integration tests for Rezku Agent"""

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