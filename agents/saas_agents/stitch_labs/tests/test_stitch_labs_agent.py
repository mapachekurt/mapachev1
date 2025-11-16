"""
Tests for Stitch Labs Agent
"""

import pytest
from agents.saas_agents.stitch_labs.agent import StitchLabsAgent, stitch_labs_agent


class TestStitchLabsAgent:
    """Test suite for Stitch Labs Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = StitchLabsAgent()
        assert agent.agent_id == "agent_1146"
        assert agent.role == "Stitch Labs Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "inventory"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = StitchLabsAgent()
        result = agent.execute("test task")
        assert "Stitch Labs Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = StitchLabsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = StitchLabsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1146"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "inventory"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert stitch_labs_agent.agent_id == "agent_1146"


class TestStitchLabsIntegration:
    """Integration tests for Stitch Labs Agent"""

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