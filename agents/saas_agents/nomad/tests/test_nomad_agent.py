"""
Tests for Nomad Agent
"""

import pytest
from agents.saas_agents.nomad.agent import NomadAgent, nomad_agent


class TestNomadAgent:
    """Test suite for Nomad Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NomadAgent()
        assert agent.agent_id == "agent_699"
        assert agent.role == "Nomad Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NomadAgent()
        result = agent.execute("test task")
        assert "Nomad Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NomadAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NomadAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_699"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nomad_agent.agent_id == "agent_699"


class TestNomadIntegration:
    """Integration tests for Nomad Agent"""

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