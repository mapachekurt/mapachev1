"""
Tests for Sage Agent
"""

import pytest
from agents.saas_agents.sage.agent import SageAgent, sage_agent


class TestSageAgent:
    """Test suite for Sage Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SageAgent()
        assert agent.agent_id == "agent_896"
        assert agent.role == "Sage Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SageAgent()
        result = agent.execute("test task")
        assert "Sage Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SageAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SageAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_896"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sage_agent.agent_id == "agent_896"


class TestSageIntegration:
    """Integration tests for Sage Agent"""

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