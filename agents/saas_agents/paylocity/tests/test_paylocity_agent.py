"""
Tests for Paylocity Agent
"""

import pytest
from agents.saas_agents.paylocity.agent import PaylocityAgent, paylocity_agent


class TestPaylocityAgent:
    """Test suite for Paylocity Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PaylocityAgent()
        assert agent.agent_id == "agent_955"
        assert agent.role == "Paylocity Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PaylocityAgent()
        result = agent.execute("test task")
        assert "Paylocity Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PaylocityAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PaylocityAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_955"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert paylocity_agent.agent_id == "agent_955"


class TestPaylocityIntegration:
    """Integration tests for Paylocity Agent"""

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