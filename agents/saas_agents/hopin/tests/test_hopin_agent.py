"""
Tests for Hopin Agent
"""

import pytest
from agents.saas_agents.hopin.agent import HopinAgent, hopin_agent


class TestHopinAgent:
    """Test suite for Hopin Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HopinAgent()
        assert agent.agent_id == "agent_1225"
        assert agent.role == "Hopin Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HopinAgent()
        result = agent.execute("test task")
        assert "Hopin Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HopinAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HopinAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1225"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hopin_agent.agent_id == "agent_1225"


class TestHopinIntegration:
    """Integration tests for Hopin Agent"""

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