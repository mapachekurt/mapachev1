"""
Tests for Omnisend Agent
"""

import pytest
from agents.saas_agents.omnisend.agent import OmnisendAgent, omnisend_agent


class TestOmnisendAgent:
    """Test suite for Omnisend Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OmnisendAgent()
        assert agent.agent_id == "agent_537"
        assert agent.role == "Omnisend Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OmnisendAgent()
        result = agent.execute("test task")
        assert "Omnisend Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OmnisendAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OmnisendAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_537"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert omnisend_agent.agent_id == "agent_537"


class TestOmnisendIntegration:
    """Integration tests for Omnisend Agent"""

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