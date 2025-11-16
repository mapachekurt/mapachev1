"""
Tests for Payoneer Agent
"""

import pytest
from agents.saas_agents.payoneer.agent import PayoneerAgent, payoneer_agent


class TestPayoneerAgent:
    """Test suite for Payoneer Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PayoneerAgent()
        assert agent.agent_id == "agent_934"
        assert agent.role == "Payoneer Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PayoneerAgent()
        result = agent.execute("test task")
        assert "Payoneer Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PayoneerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PayoneerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_934"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert payoneer_agent.agent_id == "agent_934"


class TestPayoneerIntegration:
    """Integration tests for Payoneer Agent"""

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