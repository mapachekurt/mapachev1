"""
Tests for Trulia Agent
"""

import pytest
from agents.saas_agents.trulia.agent import TruliaAgent, trulia_agent


class TestTruliaAgent:
    """Test suite for Trulia Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TruliaAgent()
        assert agent.agent_id == "agent_1075"
        assert agent.role == "Trulia Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TruliaAgent()
        result = agent.execute("test task")
        assert "Trulia Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TruliaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TruliaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1075"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert trulia_agent.agent_id == "agent_1075"


class TestTruliaIntegration:
    """Integration tests for Trulia Agent"""

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