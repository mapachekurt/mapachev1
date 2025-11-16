"""
Tests for Zillow Premier Agent Agent
"""

import pytest
from agents.saas_agents.zillow_premier.agent import ZillowPremierAgent, zillow_premier_agent


class TestZillowPremierAgent:
    """Test suite for Zillow Premier Agent Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZillowPremierAgent()
        assert agent.agent_id == "agent_1089"
        assert agent.role == "Zillow Premier Agent Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZillowPremierAgent()
        result = agent.execute("test task")
        assert "Zillow Premier Agent Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZillowPremierAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZillowPremierAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1089"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zillow_premier_agent.agent_id == "agent_1089"


class TestZillowPremierIntegration:
    """Integration tests for Zillow Premier Agent Agent"""

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