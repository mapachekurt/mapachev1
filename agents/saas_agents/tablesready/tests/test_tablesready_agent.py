"""
Tests for TablesReady Agent
"""

import pytest
from agents.saas_agents.tablesready.agent import TablesreadyAgent, tablesready_agent


class TestTablesreadyAgent:
    """Test suite for TablesReady Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TablesreadyAgent()
        assert agent.agent_id == "agent_1196"
        assert agent.role == "TablesReady Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TablesreadyAgent()
        result = agent.execute("test task")
        assert "TablesReady Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TablesreadyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TablesreadyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1196"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert tablesready_agent.agent_id == "agent_1196"


class TestTablesreadyIntegration:
    """Integration tests for TablesReady Agent"""

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