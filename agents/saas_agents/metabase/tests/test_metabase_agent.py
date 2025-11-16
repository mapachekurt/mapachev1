"""
Tests for Metabase Agent
"""

import pytest
from agents.saas_agents.metabase.agent import MetabaseAgent, metabase_agent


class TestMetabaseAgent:
    """Test suite for Metabase Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MetabaseAgent()
        assert agent.agent_id == "agent_1352"
        assert agent.role == "Metabase Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MetabaseAgent()
        result = agent.execute("test task")
        assert "Metabase Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MetabaseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MetabaseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1352"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert metabase_agent.agent_id == "agent_1352"


class TestMetabaseIntegration:
    """Integration tests for Metabase Agent"""

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