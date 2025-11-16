"""
Tests for EventMobi Agent
"""

import pytest
from agents.saas_agents.eventmobi.agent import EventmobiAgent, eventmobi_agent


class TestEventmobiAgent:
    """Test suite for EventMobi Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = EventmobiAgent()
        assert agent.agent_id == "agent_1215"
        assert agent.role == "EventMobi Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = EventmobiAgent()
        result = agent.execute("test task")
        assert "EventMobi Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = EventmobiAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = EventmobiAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1215"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert eventmobi_agent.agent_id == "agent_1215"


class TestEventmobiIntegration:
    """Integration tests for EventMobi Agent"""

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