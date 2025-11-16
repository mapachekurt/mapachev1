"""
Tests for Adapt-N Agent
"""

import pytest
from agents.saas_agents.adapt_n.agent import AdaptNAgent, adapt_n_agent


class TestAdaptNAgent:
    """Test suite for Adapt-N Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AdaptNAgent()
        assert agent.agent_id == "agent_1288"
        assert agent.role == "Adapt-N Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "agriculture"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AdaptNAgent()
        result = agent.execute("test task")
        assert "Adapt-N Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AdaptNAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AdaptNAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1288"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "agriculture"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert adapt_n_agent.agent_id == "agent_1288"


class TestAdaptNIntegration:
    """Integration tests for Adapt-N Agent"""

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