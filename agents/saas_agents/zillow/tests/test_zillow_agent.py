"""
Tests for Zillow Agent
"""

import pytest
from agents.saas_agents.zillow.agent import ZillowAgent, zillow_agent


class TestZillowAgent:
    """Test suite for Zillow Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZillowAgent()
        assert agent.agent_id == "agent_1072"
        assert agent.role == "Zillow Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZillowAgent()
        result = agent.execute("test task")
        assert "Zillow Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZillowAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZillowAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1072"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zillow_agent.agent_id == "agent_1072"


class TestZillowIntegration:
    """Integration tests for Zillow Agent"""

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