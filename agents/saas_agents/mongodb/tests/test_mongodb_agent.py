"""
Tests for MongoDB Agent
"""

import pytest
from agents.saas_agents.mongodb.agent import MongodbAgent, mongodb_agent


class TestMongodbAgent:
    """Test suite for MongoDB Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MongodbAgent()
        assert agent.agent_id == "agent_732"
        assert agent.role == "MongoDB Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "database"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MongodbAgent()
        result = agent.execute("test task")
        assert "MongoDB Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MongodbAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MongodbAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_732"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "database"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mongodb_agent.agent_id == "agent_732"


class TestMongodbIntegration:
    """Integration tests for MongoDB Agent"""

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