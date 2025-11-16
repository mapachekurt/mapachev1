"""
Tests for Fergus Agent
"""

import pytest
from agents.saas_agents.fergus.agent import FergusAgent, fergus_agent


class TestFergusAgent:
    """Test suite for Fergus Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FergusAgent()
        assert agent.agent_id == "agent_1108"
        assert agent.role == "Fergus Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FergusAgent()
        result = agent.execute("test task")
        assert "Fergus Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FergusAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FergusAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1108"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert fergus_agent.agent_id == "agent_1108"


class TestFergusIntegration:
    """Integration tests for Fergus Agent"""

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