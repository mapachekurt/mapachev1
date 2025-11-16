"""
Tests for Livestorm Agent
"""

import pytest
from agents.saas_agents.livestorm.agent import LivestormAgent, livestorm_agent


class TestLivestormAgent:
    """Test suite for Livestorm Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LivestormAgent()
        assert agent.agent_id == "agent_876"
        assert agent.role == "Livestorm Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LivestormAgent()
        result = agent.execute("test task")
        assert "Livestorm Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LivestormAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LivestormAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_876"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert livestorm_agent.agent_id == "agent_876"


class TestLivestormIntegration:
    """Integration tests for Livestorm Agent"""

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