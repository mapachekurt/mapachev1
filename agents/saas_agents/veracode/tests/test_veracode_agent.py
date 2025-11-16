"""
Tests for Veracode Agent
"""

import pytest
from agents.saas_agents.veracode.agent import VeracodeAgent, veracode_agent


class TestVeracodeAgent:
    """Test suite for Veracode Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VeracodeAgent()
        assert agent.agent_id == "agent_718"
        assert agent.role == "Veracode Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "code_quality"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VeracodeAgent()
        result = agent.execute("test task")
        assert "Veracode Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VeracodeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VeracodeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_718"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "code_quality"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert veracode_agent.agent_id == "agent_718"


class TestVeracodeIntegration:
    """Integration tests for Veracode Agent"""

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