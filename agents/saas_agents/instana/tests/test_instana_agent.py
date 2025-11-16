"""
Tests for Instana Agent
"""

import pytest
from agents.saas_agents.instana.agent import InstanaAgent, instana_agent


class TestInstanaAgent:
    """Test suite for Instana Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = InstanaAgent()
        assert agent.agent_id == "agent_686"
        assert agent.role == "Instana Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "monitoring"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = InstanaAgent()
        result = agent.execute("test task")
        assert "Instana Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = InstanaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = InstanaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_686"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "monitoring"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert instana_agent.agent_id == "agent_686"


class TestInstanaIntegration:
    """Integration tests for Instana Agent"""

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