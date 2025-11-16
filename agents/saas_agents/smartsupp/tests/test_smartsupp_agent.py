"""
Tests for Smartsupp Agent
"""

import pytest
from agents.saas_agents.smartsupp.agent import SmartsuppAgent, smartsupp_agent


class TestSmartsuppAgent:
    """Test suite for Smartsupp Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SmartsuppAgent()
        assert agent.agent_id == "agent_999"
        assert agent.role == "Smartsupp Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SmartsuppAgent()
        result = agent.execute("test task")
        assert "Smartsupp Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SmartsuppAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SmartsuppAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_999"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert smartsupp_agent.agent_id == "agent_999"


class TestSmartsuppIntegration:
    """Integration tests for Smartsupp Agent"""

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