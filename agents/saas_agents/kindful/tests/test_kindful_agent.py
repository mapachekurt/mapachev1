"""
Tests for Kindful Agent
"""

import pytest
from agents.saas_agents.kindful.agent import KindfulAgent, kindful_agent


class TestKindfulAgent:
    """Test suite for Kindful Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KindfulAgent()
        assert agent.agent_id == "agent_1260"
        assert agent.role == "Kindful Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "nonprofit"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KindfulAgent()
        result = agent.execute("test task")
        assert "Kindful Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KindfulAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KindfulAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1260"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "nonprofit"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kindful_agent.agent_id == "agent_1260"


class TestKindfulIntegration:
    """Integration tests for Kindful Agent"""

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