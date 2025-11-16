"""
Tests for Setmore Agent
"""

import pytest
from agents.saas_agents.setmore.agent import SetmoreAgent, setmore_agent


class TestSetmoreAgent:
    """Test suite for Setmore Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SetmoreAgent()
        assert agent.agent_id == "agent_851"
        assert agent.role == "Setmore Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SetmoreAgent()
        result = agent.execute("test task")
        assert "Setmore Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SetmoreAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SetmoreAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_851"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert setmore_agent.agent_id == "agent_851"


class TestSetmoreIntegration:
    """Integration tests for Setmore Agent"""

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