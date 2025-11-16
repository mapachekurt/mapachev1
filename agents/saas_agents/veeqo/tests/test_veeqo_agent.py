"""
Tests for Veeqo Agent
"""

import pytest
from agents.saas_agents.veeqo.agent import VeeqoAgent, veeqo_agent


class TestVeeqoAgent:
    """Test suite for Veeqo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VeeqoAgent()
        assert agent.agent_id == "agent_1149"
        assert agent.role == "Veeqo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VeeqoAgent()
        result = agent.execute("test task")
        assert "Veeqo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VeeqoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VeeqoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1149"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert veeqo_agent.agent_id == "agent_1149"


class TestVeeqoIntegration:
    """Integration tests for Veeqo Agent"""

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