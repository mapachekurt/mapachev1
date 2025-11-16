"""
Tests for Finicity Agent
"""

import pytest
from agents.saas_agents.finicity.agent import FinicityAgent, finicity_agent


class TestFinicityAgent:
    """Test suite for Finicity Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FinicityAgent()
        assert agent.agent_id == "agent_1503"
        assert agent.role == "Finicity Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FinicityAgent()
        result = agent.execute("test task")
        assert "Finicity Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FinicityAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FinicityAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1503"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert finicity_agent.agent_id == "agent_1503"


class TestFinicityIntegration:
    """Integration tests for Finicity Agent"""

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