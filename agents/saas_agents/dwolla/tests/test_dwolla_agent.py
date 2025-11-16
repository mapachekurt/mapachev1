"""
Tests for Dwolla Agent
"""

import pytest
from agents.saas_agents.dwolla.agent import DwollaAgent, dwolla_agent


class TestDwollaAgent:
    """Test suite for Dwolla Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DwollaAgent()
        assert agent.agent_id == "agent_1508"
        assert agent.role == "Dwolla Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DwollaAgent()
        result = agent.execute("test task")
        assert "Dwolla Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DwollaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DwollaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1508"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dwolla_agent.agent_id == "agent_1508"


class TestDwollaIntegration:
    """Integration tests for Dwolla Agent"""

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