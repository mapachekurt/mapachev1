"""
Tests for Hiver Agent
"""

import pytest
from agents.saas_agents.hiver.agent import HiverAgent, hiver_agent


class TestHiverAgent:
    """Test suite for Hiver Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HiverAgent()
        assert agent.agent_id == "agent_1009"
        assert agent.role == "Hiver Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HiverAgent()
        result = agent.execute("test task")
        assert "Hiver Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HiverAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HiverAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1009"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hiver_agent.agent_id == "agent_1009"


class TestHiverIntegration:
    """Integration tests for Hiver Agent"""

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