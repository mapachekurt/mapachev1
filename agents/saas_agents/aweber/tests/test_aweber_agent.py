"""
Tests for AWeber Agent
"""

import pytest
from agents.saas_agents.aweber.agent import AweberAgent, aweber_agent


class TestAweberAgent:
    """Test suite for AWeber Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AweberAgent()
        assert agent.agent_id == "agent_540"
        assert agent.role == "AWeber Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AweberAgent()
        result = agent.execute("test task")
        assert "AWeber Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AweberAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AweberAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_540"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aweber_agent.agent_id == "agent_540"


class TestAweberIntegration:
    """Integration tests for AWeber Agent"""

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