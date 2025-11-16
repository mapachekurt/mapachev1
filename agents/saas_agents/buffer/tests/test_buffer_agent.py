"""
Tests for Buffer Agent
"""

import pytest
from agents.saas_agents.buffer.agent import BufferAgent, buffer_agent


class TestBufferAgent:
    """Test suite for Buffer Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BufferAgent()
        assert agent.agent_id == "agent_543"
        assert agent.role == "Buffer Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "social_media"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BufferAgent()
        result = agent.execute("test task")
        assert "Buffer Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BufferAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BufferAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_543"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "social_media"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert buffer_agent.agent_id == "agent_543"


class TestBufferIntegration:
    """Integration tests for Buffer Agent"""

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