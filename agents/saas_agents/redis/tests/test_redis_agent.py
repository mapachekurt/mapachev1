"""
Tests for Redis Agent
"""

import pytest
from agents.saas_agents.redis.agent import RedisAgent, redis_agent


class TestRedisAgent:
    """Test suite for Redis Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RedisAgent()
        assert agent.agent_id == "agent_735"
        assert agent.role == "Redis Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "database"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RedisAgent()
        result = agent.execute("test task")
        assert "Redis Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RedisAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RedisAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_735"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "database"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert redis_agent.agent_id == "agent_735"


class TestRedisIntegration:
    """Integration tests for Redis Agent"""

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