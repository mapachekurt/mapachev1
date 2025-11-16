"""
Tests for Cassandra Agent
"""

import pytest
from agents.saas_agents.cassandra.agent import CassandraAgent, cassandra_agent


class TestCassandraAgent:
    """Test suite for Cassandra Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CassandraAgent()
        assert agent.agent_id == "agent_736"
        assert agent.role == "Cassandra Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "database"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CassandraAgent()
        result = agent.execute("test task")
        assert "Cassandra Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CassandraAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CassandraAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_736"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "database"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cassandra_agent.agent_id == "agent_736"


class TestCassandraIntegration:
    """Integration tests for Cassandra Agent"""

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