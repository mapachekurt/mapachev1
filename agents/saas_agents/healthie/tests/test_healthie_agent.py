"""
Tests for Healthie Agent
"""

import pytest
from agents.saas_agents.healthie.agent import HealthieAgent, healthie_agent


class TestHealthieAgent:
    """Test suite for Healthie Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HealthieAgent()
        assert agent.agent_id == "agent_1028"
        assert agent.role == "Healthie Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HealthieAgent()
        result = agent.execute("test task")
        assert "Healthie Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HealthieAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HealthieAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1028"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert healthie_agent.agent_id == "agent_1028"


class TestHealthieIntegration:
    """Integration tests for Healthie Agent"""

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