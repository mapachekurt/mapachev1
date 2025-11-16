"""
Tests for Twist Agent
"""

import pytest
from agents.saas_agents.twist.agent import TwistAgent, twist_agent


class TestTwistAgent:
    """Test suite for Twist Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TwistAgent()
        assert agent.agent_id == "agent_841"
        assert agent.role == "Twist Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TwistAgent()
        result = agent.execute("test task")
        assert "Twist Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TwistAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TwistAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_841"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert twist_agent.agent_id == "agent_841"


class TestTwistIntegration:
    """Integration tests for Twist Agent"""

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