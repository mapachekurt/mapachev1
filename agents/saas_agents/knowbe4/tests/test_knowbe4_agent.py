"""
Tests for KnowBe4 Agent
"""

import pytest
from agents.saas_agents.knowbe4.agent import Knowbe4Agent, knowbe4_agent


class TestKnowbe4Agent:
    """Test suite for KnowBe4 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = Knowbe4Agent()
        assert agent.agent_id == "agent_1442"
        assert agent.role == "KnowBe4 Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = Knowbe4Agent()
        result = agent.execute("test task")
        assert "KnowBe4 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = Knowbe4Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = Knowbe4Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1442"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert knowbe4_agent.agent_id == "agent_1442"


class TestKnowbe4Integration:
    """Integration tests for KnowBe4 Agent"""

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