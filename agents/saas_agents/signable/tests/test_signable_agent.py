"""
Tests for Signable Agent
"""

import pytest
from agents.saas_agents.signable.agent import SignableAgent, signable_agent


class TestSignableAgent:
    """Test suite for Signable Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SignableAgent()
        assert agent.agent_id == "agent_1324"
        assert agent.role == "Signable Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SignableAgent()
        result = agent.execute("test task")
        assert "Signable Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SignableAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SignableAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1324"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert signable_agent.agent_id == "agent_1324"


class TestSignableIntegration:
    """Integration tests for Signable Agent"""

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