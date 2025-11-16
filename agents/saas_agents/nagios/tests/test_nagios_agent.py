"""
Tests for Nagios Agent
"""

import pytest
from agents.saas_agents.nagios.agent import NagiosAgent, nagios_agent


class TestNagiosAgent:
    """Test suite for Nagios Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NagiosAgent()
        assert agent.agent_id == "agent_678"
        assert agent.role == "Nagios Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "monitoring"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NagiosAgent()
        result = agent.execute("test task")
        assert "Nagios Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NagiosAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NagiosAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_678"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "monitoring"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nagios_agent.agent_id == "agent_678"


class TestNagiosIntegration:
    """Integration tests for Nagios Agent"""

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