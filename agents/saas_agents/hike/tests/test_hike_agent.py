"""
Tests for Hike POS Agent
"""

import pytest
from agents.saas_agents.hike.agent import HikeAgent, hike_agent


class TestHikeAgent:
    """Test suite for Hike POS Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HikeAgent()
        assert agent.agent_id == "agent_1190"
        assert agent.role == "Hike POS Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HikeAgent()
        result = agent.execute("test task")
        assert "Hike POS Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HikeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HikeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1190"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hike_agent.agent_id == "agent_1190"


class TestHikeIntegration:
    """Integration tests for Hike POS Agent"""

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