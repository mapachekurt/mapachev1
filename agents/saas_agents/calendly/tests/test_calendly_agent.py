"""
Tests for Calendly Agent
"""

import pytest
from agents.saas_agents.calendly.agent import CalendlyAgent, calendly_agent


class TestCalendlyAgent:
    """Test suite for Calendly Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CalendlyAgent()
        assert agent.agent_id == "agent_847"
        assert agent.role == "Calendly Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CalendlyAgent()
        result = agent.execute("test task")
        assert "Calendly Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CalendlyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CalendlyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_847"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert calendly_agent.agent_id == "agent_847"


class TestCalendlyIntegration:
    """Integration tests for Calendly Agent"""

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