"""
Tests for Mindbody Agent
"""

import pytest
from agents.saas_agents.mindbody.agent import MindbodyAgent, mindbody_agent


class TestMindbodyAgent:
    """Test suite for Mindbody Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MindbodyAgent()
        assert agent.agent_id == "agent_1029"
        assert agent.role == "Mindbody Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MindbodyAgent()
        result = agent.execute("test task")
        assert "Mindbody Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MindbodyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MindbodyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1029"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mindbody_agent.agent_id == "agent_1029"


class TestMindbodyIntegration:
    """Integration tests for Mindbody Agent"""

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