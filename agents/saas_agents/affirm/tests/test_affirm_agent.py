"""
Tests for Affirm Agent
"""

import pytest
from agents.saas_agents.affirm.agent import AffirmAgent, affirm_agent


class TestAffirmAgent:
    """Test suite for Affirm Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AffirmAgent()
        assert agent.agent_id == "agent_932"
        assert agent.role == "Affirm Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AffirmAgent()
        result = agent.execute("test task")
        assert "Affirm Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AffirmAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AffirmAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_932"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert affirm_agent.agent_id == "agent_932"


class TestAffirmIntegration:
    """Integration tests for Affirm Agent"""

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