"""
Tests for Linnworks Agent
"""

import pytest
from agents.saas_agents.linnworks.agent import LinnworksAgent, linnworks_agent


class TestLinnworksAgent:
    """Test suite for Linnworks Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LinnworksAgent()
        assert agent.agent_id == "agent_1148"
        assert agent.role == "Linnworks Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LinnworksAgent()
        result = agent.execute("test task")
        assert "Linnworks Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LinnworksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LinnworksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1148"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert linnworks_agent.agent_id == "agent_1148"


class TestLinnworksIntegration:
    """Integration tests for Linnworks Agent"""

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