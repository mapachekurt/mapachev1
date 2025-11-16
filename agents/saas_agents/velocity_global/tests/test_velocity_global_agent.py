"""
Tests for Velocity Global Agent
"""

import pytest
from agents.saas_agents.velocity_global.agent import VelocityGlobalAgent, velocity_global_agent


class TestVelocityGlobalAgent:
    """Test suite for Velocity Global Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VelocityGlobalAgent()
        assert agent.agent_id == "agent_966"
        assert agent.role == "Velocity Global Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VelocityGlobalAgent()
        result = agent.execute("test task")
        assert "Velocity Global Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VelocityGlobalAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VelocityGlobalAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_966"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert velocity_global_agent.agent_id == "agent_966"


class TestVelocityGlobalIntegration:
    """Integration tests for Velocity Global Agent"""

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