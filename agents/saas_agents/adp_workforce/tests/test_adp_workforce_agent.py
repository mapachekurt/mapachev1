"""
Tests for ADP Workforce Now Agent
"""

import pytest
from agents.saas_agents.adp_workforce.agent import AdpWorkforceAgent, adp_workforce_agent


class TestAdpWorkforceAgent:
    """Test suite for ADP Workforce Now Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AdpWorkforceAgent()
        assert agent.agent_id == "agent_953"
        assert agent.role == "ADP Workforce Now Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AdpWorkforceAgent()
        result = agent.execute("test task")
        assert "ADP Workforce Now Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AdpWorkforceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AdpWorkforceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_953"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert adp_workforce_agent.agent_id == "agent_953"


class TestAdpWorkforceIntegration:
    """Integration tests for ADP Workforce Now Agent"""

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