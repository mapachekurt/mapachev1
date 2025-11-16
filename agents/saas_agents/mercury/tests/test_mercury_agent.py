"""
Tests for Mercury Agent
"""

import pytest
from agents.saas_agents.mercury.agent import MercuryAgent, mercury_agent


class TestMercuryAgent:
    """Test suite for Mercury Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MercuryAgent()
        assert agent.agent_id == "agent_938"
        assert agent.role == "Mercury Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MercuryAgent()
        result = agent.execute("test task")
        assert "Mercury Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MercuryAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MercuryAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_938"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mercury_agent.agent_id == "agent_938"


class TestMercuryIntegration:
    """Integration tests for Mercury Agent"""

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