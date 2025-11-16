"""
Tests for Clarizen Agent
"""

import pytest
from agents.saas_agents.clarizen.agent import ClarizenAgent, clarizen_agent


class TestClarizenAgent:
    """Test suite for Clarizen Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ClarizenAgent()
        assert agent.agent_id == "agent_809"
        assert agent.role == "Clarizen Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ClarizenAgent()
        result = agent.execute("test task")
        assert "Clarizen Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ClarizenAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ClarizenAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_809"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert clarizen_agent.agent_id == "agent_809"


class TestClarizenIntegration:
    """Integration tests for Clarizen Agent"""

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