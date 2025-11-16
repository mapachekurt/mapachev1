"""
Tests for Increase Agent
"""

import pytest
from agents.saas_agents.increase.agent import IncreaseAgent, increase_agent


class TestIncreaseAgent:
    """Test suite for Increase Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = IncreaseAgent()
        assert agent.agent_id == "agent_1511"
        assert agent.role == "Increase Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = IncreaseAgent()
        result = agent.execute("test task")
        assert "Increase Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = IncreaseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = IncreaseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1511"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert increase_agent.agent_id == "agent_1511"


class TestIncreaseIntegration:
    """Integration tests for Increase Agent"""

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