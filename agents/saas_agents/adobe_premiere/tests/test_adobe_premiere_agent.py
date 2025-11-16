"""
Tests for Adobe Premiere Pro Agent
"""

import pytest
from agents.saas_agents.adobe_premiere.agent import AdobePremiereAgent, adobe_premiere_agent


class TestAdobePremiereAgent:
    """Test suite for Adobe Premiere Pro Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AdobePremiereAgent()
        assert agent.agent_id == "agent_767"
        assert agent.role == "Adobe Premiere Pro Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AdobePremiereAgent()
        result = agent.execute("test task")
        assert "Adobe Premiere Pro Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AdobePremiereAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AdobePremiereAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_767"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert adobe_premiere_agent.agent_id == "agent_767"


class TestAdobePremiereIntegration:
    """Integration tests for Adobe Premiere Pro Agent"""

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