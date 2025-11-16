"""
Tests for Flywire Agent
"""

import pytest
from agents.saas_agents.flywire.agent import FlywireAgent, flywire_agent


class TestFlywireAgent:
    """Test suite for Flywire Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FlywireAgent()
        assert agent.agent_id == "agent_1499"
        assert agent.role == "Flywire Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FlywireAgent()
        result = agent.execute("test task")
        assert "Flywire Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FlywireAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FlywireAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1499"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert flywire_agent.agent_id == "agent_1499"


class TestFlywireIntegration:
    """Integration tests for Flywire Agent"""

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