"""
Tests for Bear Agent
"""

import pytest
from agents.saas_agents.bear.agent import BearAgent, bear_agent


class TestBearAgent:
    """Test suite for Bear Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BearAgent()
        assert agent.agent_id == "agent_744"
        assert agent.role == "Bear Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "notes"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BearAgent()
        result = agent.execute("test task")
        assert "Bear Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BearAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BearAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_744"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "notes"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bear_agent.agent_id == "agent_744"


class TestBearIntegration:
    """Integration tests for Bear Agent"""

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