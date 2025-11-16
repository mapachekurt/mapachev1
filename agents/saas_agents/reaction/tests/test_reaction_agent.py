"""
Tests for Reaction Commerce Agent
"""

import pytest
from agents.saas_agents.reaction.agent import ReactionAgent, reaction_agent


class TestReactionAgent:
    """Test suite for Reaction Commerce Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ReactionAgent()
        assert agent.agent_id == "agent_984"
        assert agent.role == "Reaction Commerce Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ReactionAgent()
        result = agent.execute("test task")
        assert "Reaction Commerce Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ReactionAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ReactionAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_984"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert reaction_agent.agent_id == "agent_984"


class TestReactionIntegration:
    """Integration tests for Reaction Commerce Agent"""

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