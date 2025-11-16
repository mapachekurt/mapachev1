"""
Tests for Flood.io Agent
"""

import pytest
from agents.saas_agents.flood_io.agent import FloodIoAgent, flood_io_agent


class TestFloodIoAgent:
    """Test suite for Flood.io Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FloodIoAgent()
        assert agent.agent_id == "agent_1409"
        assert agent.role == "Flood.io Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FloodIoAgent()
        result = agent.execute("test task")
        assert "Flood.io Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FloodIoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FloodIoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1409"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert flood_io_agent.agent_id == "agent_1409"


class TestFloodIoIntegration:
    """Integration tests for Flood.io Agent"""

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