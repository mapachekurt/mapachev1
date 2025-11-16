"""
Tests for Sketch Agent
"""

import pytest
from agents.saas_agents.sketch.agent import SketchAgent, sketch_agent


class TestSketchAgent:
    """Test suite for Sketch Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SketchAgent()
        assert agent.agent_id == "agent_758"
        assert agent.role == "Sketch Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SketchAgent()
        result = agent.execute("test task")
        assert "Sketch Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SketchAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SketchAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_758"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sketch_agent.agent_id == "agent_758"


class TestSketchIntegration:
    """Integration tests for Sketch Agent"""

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