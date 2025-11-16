"""
Tests for MuleSoft Agent
"""

import pytest
from agents.saas_agents.mulesoft.agent import MulesoftAgent, mulesoft_agent


class TestMulesoftAgent:
    """Test suite for MuleSoft Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MulesoftAgent()
        assert agent.agent_id == "agent_706"
        assert agent.role == "MuleSoft Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "api"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MulesoftAgent()
        result = agent.execute("test task")
        assert "MuleSoft Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MulesoftAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MulesoftAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_706"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "api"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mulesoft_agent.agent_id == "agent_706"


class TestMulesoftIntegration:
    """Integration tests for MuleSoft Agent"""

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