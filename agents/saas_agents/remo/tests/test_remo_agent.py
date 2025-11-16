"""
Tests for Remo Agent
"""

import pytest
from agents.saas_agents.remo.agent import RemoAgent, remo_agent


class TestRemoAgent:
    """Test suite for Remo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RemoAgent()
        assert agent.agent_id == "agent_1231"
        assert agent.role == "Remo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RemoAgent()
        result = agent.execute("test task")
        assert "Remo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RemoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RemoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1231"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert remo_agent.agent_id == "agent_1231"


class TestRemoIntegration:
    """Integration tests for Remo Agent"""

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