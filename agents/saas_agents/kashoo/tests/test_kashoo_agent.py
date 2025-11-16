"""
Tests for Kashoo Agent
"""

import pytest
from agents.saas_agents.kashoo.agent import KashooAgent, kashoo_agent


class TestKashooAgent:
    """Test suite for Kashoo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KashooAgent()
        assert agent.agent_id == "agent_897"
        assert agent.role == "Kashoo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KashooAgent()
        result = agent.execute("test task")
        assert "Kashoo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KashooAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KashooAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_897"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kashoo_agent.agent_id == "agent_897"


class TestKashooIntegration:
    """Integration tests for Kashoo Agent"""

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