"""
Tests for ThoughtSpot Agent
"""

import pytest
from agents.saas_agents.thoughtspot.agent import ThoughtspotAgent, thoughtspot_agent


class TestThoughtspotAgent:
    """Test suite for ThoughtSpot Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ThoughtspotAgent()
        assert agent.agent_id == "agent_1365"
        assert agent.role == "ThoughtSpot Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ThoughtspotAgent()
        result = agent.execute("test task")
        assert "ThoughtSpot Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ThoughtspotAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ThoughtspotAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1365"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert thoughtspot_agent.agent_id == "agent_1365"


class TestThoughtspotIntegration:
    """Integration tests for ThoughtSpot Agent"""

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