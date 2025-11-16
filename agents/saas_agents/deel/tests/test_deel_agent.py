"""
Tests for Deel Agent
"""

import pytest
from agents.saas_agents.deel.agent import DeelAgent, deel_agent


class TestDeelAgent:
    """Test suite for Deel Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DeelAgent()
        assert agent.agent_id == "agent_960"
        assert agent.role == "Deel Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DeelAgent()
        result = agent.execute("test task")
        assert "Deel Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DeelAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DeelAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_960"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert deel_agent.agent_id == "agent_960"


class TestDeelIntegration:
    """Integration tests for Deel Agent"""

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