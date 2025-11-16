"""
Tests for Linear Agent
"""

import pytest
from agents.saas_agents.linear.agent import LinearAgent, linear_agent


class TestLinearAgent:
    """Test suite for Linear Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LinearAgent()
        assert agent.agent_id == "agent_525"
        assert agent.role == "Linear Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LinearAgent()
        result = agent.execute("test task")
        assert "Linear Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LinearAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LinearAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_525"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert linear_agent.agent_id == "agent_525"


class TestLinearIntegration:
    """Integration tests for Linear Agent"""

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