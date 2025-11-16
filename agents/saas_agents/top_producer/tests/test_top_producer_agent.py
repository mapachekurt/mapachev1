"""
Tests for Top Producer Agent
"""

import pytest
from agents.saas_agents.top_producer.agent import TopProducerAgent, top_producer_agent


class TestTopProducerAgent:
    """Test suite for Top Producer Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TopProducerAgent()
        assert agent.agent_id == "agent_1084"
        assert agent.role == "Top Producer Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TopProducerAgent()
        result = agent.execute("test task")
        assert "Top Producer Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TopProducerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TopProducerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1084"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert top_producer_agent.agent_id == "agent_1084"


class TestTopProducerIntegration:
    """Integration tests for Top Producer Agent"""

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