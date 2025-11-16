"""
Tests for Adobe After Effects Agent
"""

import pytest
from agents.saas_agents.adobe_after_effects.agent import AdobeAfterEffectsAgent, adobe_after_effects_agent


class TestAdobeAfterEffectsAgent:
    """Test suite for Adobe After Effects Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AdobeAfterEffectsAgent()
        assert agent.agent_id == "agent_768"
        assert agent.role == "Adobe After Effects Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AdobeAfterEffectsAgent()
        result = agent.execute("test task")
        assert "Adobe After Effects Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AdobeAfterEffectsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AdobeAfterEffectsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_768"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert adobe_after_effects_agent.agent_id == "agent_768"


class TestAdobeAfterEffectsIntegration:
    """Integration tests for Adobe After Effects Agent"""

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