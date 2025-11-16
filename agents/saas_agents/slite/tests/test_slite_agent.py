"""
Tests for Slite Agent
"""

import pytest
from agents.saas_agents.slite.agent import SliteAgent, slite_agent


class TestSliteAgent:
    """Test suite for Slite Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SliteAgent()
        assert agent.agent_id == "agent_783"
        assert agent.role == "Slite Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SliteAgent()
        result = agent.execute("test task")
        assert "Slite Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SliteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SliteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_783"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert slite_agent.agent_id == "agent_783"


class TestSliteIntegration:
    """Integration tests for Slite Agent"""

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