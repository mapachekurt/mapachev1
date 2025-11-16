"""
Tests for Canva Agent
"""

import pytest
from agents.saas_agents.canva.agent import CanvaAgent, canva_agent


class TestCanvaAgent:
    """Test suite for Canva Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CanvaAgent()
        assert agent.agent_id == "agent_763"
        assert agent.role == "Canva Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CanvaAgent()
        result = agent.execute("test task")
        assert "Canva Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CanvaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CanvaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_763"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert canva_agent.agent_id == "agent_763"


class TestCanvaIntegration:
    """Integration tests for Canva Agent"""

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