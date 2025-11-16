"""
Tests for Grammarly Agent
"""

import pytest
from agents.saas_agents.grammarly.agent import GrammarlyAgent, grammarly_agent


class TestGrammarlyAgent:
    """Test suite for Grammarly Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GrammarlyAgent()
        assert agent.agent_id == "agent_1312"
        assert agent.role == "Grammarly Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GrammarlyAgent()
        result = agent.execute("test task")
        assert "Grammarly Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GrammarlyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GrammarlyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1312"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert grammarly_agent.agent_id == "agent_1312"


class TestGrammarlyIntegration:
    """Integration tests for Grammarly Agent"""

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