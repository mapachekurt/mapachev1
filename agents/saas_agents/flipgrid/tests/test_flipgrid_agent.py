"""
Tests for Flipgrid Agent
"""

import pytest
from agents.saas_agents.flipgrid.agent import FlipgridAgent, flipgrid_agent


class TestFlipgridAgent:
    """Test suite for Flipgrid Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FlipgridAgent()
        assert agent.agent_id == "agent_1069"
        assert agent.role == "Flipgrid Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FlipgridAgent()
        result = agent.execute("test task")
        assert "Flipgrid Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FlipgridAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FlipgridAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1069"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert flipgrid_agent.agent_id == "agent_1069"


class TestFlipgridIntegration:
    """Integration tests for Flipgrid Agent"""

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