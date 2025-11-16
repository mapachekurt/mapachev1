"""
Tests for Lightstep Agent
"""

import pytest
from agents.saas_agents.lightstep.agent import LightstepAgent, lightstep_agent


class TestLightstepAgent:
    """Test suite for Lightstep Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LightstepAgent()
        assert agent.agent_id == "agent_685"
        assert agent.role == "Lightstep Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "monitoring"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LightstepAgent()
        result = agent.execute("test task")
        assert "Lightstep Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LightstepAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LightstepAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_685"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "monitoring"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lightstep_agent.agent_id == "agent_685"


class TestLightstepIntegration:
    """Integration tests for Lightstep Agent"""

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