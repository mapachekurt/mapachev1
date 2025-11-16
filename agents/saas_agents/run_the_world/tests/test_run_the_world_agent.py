"""
Tests for Run the World Agent
"""

import pytest
from agents.saas_agents.run_the_world.agent import RunTheWorldAgent, run_the_world_agent


class TestRunTheWorldAgent:
    """Test suite for Run the World Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RunTheWorldAgent()
        assert agent.agent_id == "agent_1226"
        assert agent.role == "Run the World Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RunTheWorldAgent()
        result = agent.execute("test task")
        assert "Run the World Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RunTheWorldAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RunTheWorldAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1226"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert run_the_world_agent.agent_id == "agent_1226"


class TestRunTheWorldIntegration:
    """Integration tests for Run the World Agent"""

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