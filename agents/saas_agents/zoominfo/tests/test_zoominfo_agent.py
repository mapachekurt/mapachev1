"""
Tests for ZoomInfo Agent
"""

import pytest
from agents.saas_agents.zoominfo.agent import ZoominfoAgent, zoominfo_agent


class TestZoominfoAgent:
    """Test suite for ZoomInfo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZoominfoAgent()
        assert agent.agent_id == "agent_614"
        assert agent.role == "ZoomInfo Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZoominfoAgent()
        result = agent.execute("test task")
        assert "ZoomInfo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZoominfoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZoominfoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_614"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zoominfo_agent.agent_id == "agent_614"


class TestZoominfoIntegration:
    """Integration tests for ZoomInfo Agent"""

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