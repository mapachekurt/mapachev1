"""
Tests for Nearpod Agent
"""

import pytest
from agents.saas_agents.nearpod.agent import NearpodAgent, nearpod_agent


class TestNearpodAgent:
    """Test suite for Nearpod Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NearpodAgent()
        assert agent.agent_id == "agent_1061"
        assert agent.role == "Nearpod Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NearpodAgent()
        result = agent.execute("test task")
        assert "Nearpod Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NearpodAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NearpodAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1061"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nearpod_agent.agent_id == "agent_1061"


class TestNearpodIntegration:
    """Integration tests for Nearpod Agent"""

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