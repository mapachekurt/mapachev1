"""
Tests for Revel Systems Agent
"""

import pytest
from agents.saas_agents.revel.agent import RevelAgent, revel_agent


class TestRevelAgent:
    """Test suite for Revel Systems Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RevelAgent()
        assert agent.agent_id == "agent_1156"
        assert agent.role == "Revel Systems Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RevelAgent()
        result = agent.execute("test task")
        assert "Revel Systems Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RevelAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RevelAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1156"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert revel_agent.agent_id == "agent_1156"


class TestRevelIntegration:
    """Integration tests for Revel Systems Agent"""

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