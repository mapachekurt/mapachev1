"""
Tests for Ahrefs Agent
"""

import pytest
from agents.saas_agents.ahrefs.agent import AhrefsAgent, ahrefs_agent


class TestAhrefsAgent:
    """Test suite for Ahrefs Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AhrefsAgent()
        assert agent.agent_id == "agent_553"
        assert agent.role == "Ahrefs Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "seo"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AhrefsAgent()
        result = agent.execute("test task")
        assert "Ahrefs Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AhrefsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AhrefsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_553"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "seo"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ahrefs_agent.agent_id == "agent_553"


class TestAhrefsIntegration:
    """Integration tests for Ahrefs Agent"""

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