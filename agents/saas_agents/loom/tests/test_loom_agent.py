"""
Tests for Loom Agent
"""

import pytest
from agents.saas_agents.loom.agent import LoomAgent, loom_agent


class TestLoomAgent:
    """Test suite for Loom Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LoomAgent()
        assert agent.agent_id == "agent_1070"
        assert agent.role == "Loom Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LoomAgent()
        result = agent.execute("test task")
        assert "Loom Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LoomAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LoomAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1070"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert loom_agent.agent_id == "agent_1070"


class TestLoomIntegration:
    """Integration tests for Loom Agent"""

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