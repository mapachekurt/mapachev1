"""
Tests for ElevenLabs Agent
"""

import pytest
from agents.saas_agents.elevenlabs.agent import ElevenlabsAgent, elevenlabs_agent


class TestElevenlabsAgent:
    """Test suite for ElevenLabs Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ElevenlabsAgent()
        assert agent.agent_id == "agent_1460"
        assert agent.role == "ElevenLabs Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ai"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ElevenlabsAgent()
        result = agent.execute("test task")
        assert "ElevenLabs Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ElevenlabsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ElevenlabsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1460"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ai"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert elevenlabs_agent.agent_id == "agent_1460"


class TestElevenlabsIntegration:
    """Integration tests for ElevenLabs Agent"""

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