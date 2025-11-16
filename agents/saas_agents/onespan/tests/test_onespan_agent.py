"""
Tests for OneSpan Sign Agent
"""

import pytest
from agents.saas_agents.onespan.agent import OnespanAgent, onespan_agent


class TestOnespanAgent:
    """Test suite for OneSpan Sign Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OnespanAgent()
        assert agent.agent_id == "agent_1325"
        assert agent.role == "OneSpan Sign Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OnespanAgent()
        result = agent.execute("test task")
        assert "OneSpan Sign Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OnespanAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OnespanAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1325"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert onespan_agent.agent_id == "agent_1325"


class TestOnespanIntegration:
    """Integration tests for OneSpan Sign Agent"""

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