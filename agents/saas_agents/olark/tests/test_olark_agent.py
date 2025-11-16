"""
Tests for Olark Agent
"""

import pytest
from agents.saas_agents.olark.agent import OlarkAgent, olark_agent


class TestOlarkAgent:
    """Test suite for Olark Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OlarkAgent()
        assert agent.agent_id == "agent_996"
        assert agent.role == "Olark Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OlarkAgent()
        result = agent.execute("test task")
        assert "Olark Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OlarkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OlarkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_996"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert olark_agent.agent_id == "agent_996"


class TestOlarkIntegration:
    """Integration tests for Olark Agent"""

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