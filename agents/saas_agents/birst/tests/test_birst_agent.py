"""
Tests for Birst Agent
"""

import pytest
from agents.saas_agents.birst.agent import BirstAgent, birst_agent


class TestBirstAgent:
    """Test suite for Birst Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BirstAgent()
        assert agent.agent_id == "agent_1363"
        assert agent.role == "Birst Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BirstAgent()
        result = agent.execute("test task")
        assert "Birst Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BirstAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BirstAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1363"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert birst_agent.agent_id == "agent_1363"


class TestBirstIntegration:
    """Integration tests for Birst Agent"""

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