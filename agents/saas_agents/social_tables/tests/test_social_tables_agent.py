"""
Tests for Social Tables Agent
"""

import pytest
from agents.saas_agents.social_tables.agent import SocialTablesAgent, social_tables_agent


class TestSocialTablesAgent:
    """Test suite for Social Tables Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SocialTablesAgent()
        assert agent.agent_id == "agent_1219"
        assert agent.role == "Social Tables Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "events"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SocialTablesAgent()
        result = agent.execute("test task")
        assert "Social Tables Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SocialTablesAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SocialTablesAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1219"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "events"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert social_tables_agent.agent_id == "agent_1219"


class TestSocialTablesIntegration:
    """Integration tests for Social Tables Agent"""

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