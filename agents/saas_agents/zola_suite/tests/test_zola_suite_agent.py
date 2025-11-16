"""
Tests for Zola Suite Agent
"""

import pytest
from agents.saas_agents.zola_suite.agent import ZolaSuiteAgent, zola_suite_agent


class TestZolaSuiteAgent:
    """Test suite for Zola Suite Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZolaSuiteAgent()
        assert agent.agent_id == "agent_1042"
        assert agent.role == "Zola Suite Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZolaSuiteAgent()
        result = agent.execute("test task")
        assert "Zola Suite Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZolaSuiteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZolaSuiteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1042"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zola_suite_agent.agent_id == "agent_1042"


class TestZolaSuiteIntegration:
    """Integration tests for Zola Suite Agent"""

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