"""
Tests for N26 Business Agent
"""

import pytest
from agents.saas_agents.n26.agent import N26Agent, n26_agent


class TestN26Agent:
    """Test suite for N26 Business Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = N26Agent()
        assert agent.agent_id == "agent_937"
        assert agent.role == "N26 Business Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "payments"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = N26Agent()
        result = agent.execute("test task")
        assert "N26 Business Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = N26Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = N26Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_937"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "payments"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert n26_agent.agent_id == "agent_937"


class TestN26Integration:
    """Integration tests for N26 Business Agent"""

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