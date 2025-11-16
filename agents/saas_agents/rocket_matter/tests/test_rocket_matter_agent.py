"""
Tests for Rocket Matter Agent
"""

import pytest
from agents.saas_agents.rocket_matter.agent import RocketMatterAgent, rocket_matter_agent


class TestRocketMatterAgent:
    """Test suite for Rocket Matter Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RocketMatterAgent()
        assert agent.agent_id == "agent_1035"
        assert agent.role == "Rocket Matter Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RocketMatterAgent()
        result = agent.execute("test task")
        assert "Rocket Matter Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RocketMatterAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RocketMatterAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1035"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rocket_matter_agent.agent_id == "agent_1035"


class TestRocketMatterIntegration:
    """Integration tests for Rocket Matter Agent"""

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