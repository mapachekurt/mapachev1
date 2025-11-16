"""
Tests for Adobe Illustrator Agent
"""

import pytest
from agents.saas_agents.adobe_illustrator.agent import AdobeIllustratorAgent, adobe_illustrator_agent


class TestAdobeIllustratorAgent:
    """Test suite for Adobe Illustrator Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AdobeIllustratorAgent()
        assert agent.agent_id == "agent_765"
        assert agent.role == "Adobe Illustrator Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AdobeIllustratorAgent()
        result = agent.execute("test task")
        assert "Adobe Illustrator Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AdobeIllustratorAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AdobeIllustratorAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_765"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert adobe_illustrator_agent.agent_id == "agent_765"


class TestAdobeIllustratorIntegration:
    """Integration tests for Adobe Illustrator Agent"""

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