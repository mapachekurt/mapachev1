"""
Tests for GnuCash Agent
"""

import pytest
from agents.saas_agents.gnucash.agent import GnucashAgent, gnucash_agent


class TestGnucashAgent:
    """Test suite for GnuCash Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GnucashAgent()
        assert agent.agent_id == "agent_906"
        assert agent.role == "GnuCash Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GnucashAgent()
        result = agent.execute("test task")
        assert "GnuCash Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GnucashAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GnucashAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_906"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gnucash_agent.agent_id == "agent_906"


class TestGnucashIntegration:
    """Integration tests for GnuCash Agent"""

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