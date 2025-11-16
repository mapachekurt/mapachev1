"""
Tests for Hubilo Agent
"""

import pytest
from agents.saas_agents.hubilo.agent import HubiloAgent, hubilo_agent


class TestHubiloAgent:
    """Test suite for Hubilo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HubiloAgent()
        assert agent.agent_id == "agent_1224"
        assert agent.role == "Hubilo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HubiloAgent()
        result = agent.execute("test task")
        assert "Hubilo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HubiloAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HubiloAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1224"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hubilo_agent.agent_id == "agent_1224"


class TestHubiloIntegration:
    """Integration tests for Hubilo Agent"""

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