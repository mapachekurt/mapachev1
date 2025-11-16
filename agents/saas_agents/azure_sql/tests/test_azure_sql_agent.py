"""
Tests for Azure SQL Agent
"""

import pytest
from agents.saas_agents.azure_sql.agent import AzureSqlAgent, azure_sql_agent


class TestAzureSqlAgent:
    """Test suite for Azure SQL Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureSqlAgent()
        assert agent.agent_id == "agent_655"
        assert agent.role == "Azure SQL Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureSqlAgent()
        result = agent.execute("test task")
        assert "Azure SQL Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureSqlAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureSqlAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_655"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_sql_agent.agent_id == "agent_655"


class TestAzureSqlIntegration:
    """Integration tests for Azure SQL Agent"""

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