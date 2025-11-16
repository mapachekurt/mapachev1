"""
Tests for Revolut Business Agent
"""

import pytest
from agents.saas_agents.revolut.agent import RevolutAgent, revolut_agent


class TestRevolutAgent:
    """Test suite for Revolut Business Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RevolutAgent()
        assert agent.agent_id == "agent_936"
        assert agent.role == "Revolut Business Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RevolutAgent()
        result = agent.execute("test task")
        assert "Revolut Business Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RevolutAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RevolutAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_936"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert revolut_agent.agent_id == "agent_936"


class TestRevolutIntegration:
    """Integration tests for Revolut Business Agent"""

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