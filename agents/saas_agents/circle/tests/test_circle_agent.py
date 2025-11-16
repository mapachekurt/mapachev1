"""
Tests for Circle Agent
"""

import pytest
from agents.saas_agents.circle.agent import CircleAgent, circle_agent


class TestCircleAgent:
    """Test suite for Circle Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CircleAgent()
        assert agent.agent_id == "agent_1249"
        assert agent.role == "Circle Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "membership"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CircleAgent()
        result = agent.execute("test task")
        assert "Circle Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CircleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CircleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1249"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "membership"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert circle_agent.agent_id == "agent_1249"


class TestCircleIntegration:
    """Integration tests for Circle Agent"""

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