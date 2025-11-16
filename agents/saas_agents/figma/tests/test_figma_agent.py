"""
Tests for Figma Agent
"""

import pytest
from agents.saas_agents.figma.agent import FigmaAgent, figma_agent


class TestFigmaAgent:
    """Test suite for Figma Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FigmaAgent()
        assert agent.agent_id == "agent_757"
        assert agent.role == "Figma Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FigmaAgent()
        result = agent.execute("test task")
        assert "Figma Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FigmaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FigmaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_757"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert figma_agent.agent_id == "agent_757"


class TestFigmaIntegration:
    """Integration tests for Figma Agent"""

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