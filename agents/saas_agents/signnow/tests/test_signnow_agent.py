"""
Tests for SignNow Agent
"""

import pytest
from agents.saas_agents.signnow.agent import SignnowAgent, signnow_agent


class TestSignnowAgent:
    """Test suite for SignNow Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SignnowAgent()
        assert agent.agent_id == "agent_1320"
        assert agent.role == "SignNow Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SignnowAgent()
        result = agent.execute("test task")
        assert "SignNow Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SignnowAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SignnowAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1320"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert signnow_agent.agent_id == "agent_1320"


class TestSignnowIntegration:
    """Integration tests for SignNow Agent"""

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