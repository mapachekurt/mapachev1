"""
Tests for RingCentral Video Agent
"""

import pytest
from agents.saas_agents.ringcentral.agent import RingcentralAgent, ringcentral_agent


class TestRingcentralAgent:
    """Test suite for RingCentral Video Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RingcentralAgent()
        assert agent.agent_id == "agent_869"
        assert agent.role == "RingCentral Video Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RingcentralAgent()
        result = agent.execute("test task")
        assert "RingCentral Video Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RingcentralAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RingcentralAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_869"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ringcentral_agent.agent_id == "agent_869"


class TestRingcentralIntegration:
    """Integration tests for RingCentral Video Agent"""

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