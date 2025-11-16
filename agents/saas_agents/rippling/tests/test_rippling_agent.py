"""
Tests for Rippling Agent
"""

import pytest
from agents.saas_agents.rippling.agent import RipplingAgent, rippling_agent


class TestRipplingAgent:
    """Test suite for Rippling Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RipplingAgent()
        assert agent.agent_id == "agent_957"
        assert agent.role == "Rippling Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RipplingAgent()
        result = agent.execute("test task")
        assert "Rippling Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RipplingAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RipplingAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_957"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rippling_agent.agent_id == "agent_957"


class TestRipplingIntegration:
    """Integration tests for Rippling Agent"""

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