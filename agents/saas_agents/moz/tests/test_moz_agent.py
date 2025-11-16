"""
Tests for Moz Agent
"""

import pytest
from agents.saas_agents.moz.agent import MozAgent, moz_agent


class TestMozAgent:
    """Test suite for Moz Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MozAgent()
        assert agent.agent_id == "agent_554"
        assert agent.role == "Moz Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "seo"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MozAgent()
        result = agent.execute("test task")
        assert "Moz Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MozAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MozAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_554"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "seo"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert moz_agent.agent_id == "agent_554"


class TestMozIntegration:
    """Integration tests for Moz Agent"""

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