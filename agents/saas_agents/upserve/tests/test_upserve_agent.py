"""
Tests for Upserve Agent
"""

import pytest
from agents.saas_agents.upserve.agent import UpserveAgent, upserve_agent


class TestUpserveAgent:
    """Test suite for Upserve Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = UpserveAgent()
        assert agent.agent_id == "agent_1155"
        assert agent.role == "Upserve Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = UpserveAgent()
        result = agent.execute("test task")
        assert "Upserve Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = UpserveAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = UpserveAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1155"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert upserve_agent.agent_id == "agent_1155"


class TestUpserveIntegration:
    """Integration tests for Upserve Agent"""

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