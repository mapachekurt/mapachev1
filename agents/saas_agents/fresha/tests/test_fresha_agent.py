"""
Tests for Fresha Agent
"""

import pytest
from agents.saas_agents.fresha.agent import FreshaAgent, fresha_agent


class TestFreshaAgent:
    """Test suite for Fresha Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FreshaAgent()
        assert agent.agent_id == "agent_1211"
        assert agent.role == "Fresha Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FreshaAgent()
        result = agent.execute("test task")
        assert "Fresha Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FreshaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FreshaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1211"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert fresha_agent.agent_id == "agent_1211"


class TestFreshaIntegration:
    """Integration tests for Fresha Agent"""

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