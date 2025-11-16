"""
Tests for Periscope Data Agent
"""

import pytest
from agents.saas_agents.periscope.agent import PeriscopeAgent, periscope_agent


class TestPeriscopeAgent:
    """Test suite for Periscope Data Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PeriscopeAgent()
        assert agent.agent_id == "agent_1357"
        assert agent.role == "Periscope Data Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PeriscopeAgent()
        result = agent.execute("test task")
        assert "Periscope Data Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PeriscopeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PeriscopeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1357"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert periscope_agent.agent_id == "agent_1357"


class TestPeriscopeIntegration:
    """Integration tests for Periscope Data Agent"""

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