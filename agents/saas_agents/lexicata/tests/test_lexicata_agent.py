"""
Tests for Lexicata Agent
"""

import pytest
from agents.saas_agents.lexicata.agent import LexicataAgent, lexicata_agent


class TestLexicataAgent:
    """Test suite for Lexicata Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LexicataAgent()
        assert agent.agent_id == "agent_1043"
        assert agent.role == "Lexicata Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LexicataAgent()
        result = agent.execute("test task")
        assert "Lexicata Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LexicataAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LexicataAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1043"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lexicata_agent.agent_id == "agent_1043"


class TestLexicataIntegration:
    """Integration tests for Lexicata Agent"""

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