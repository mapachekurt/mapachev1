"""
Tests for Whereby Agent
"""

import pytest
from agents.saas_agents.whereby.agent import WherebyAgent, whereby_agent


class TestWherebyAgent:
    """Test suite for Whereby Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WherebyAgent()
        assert agent.agent_id == "agent_862"
        assert agent.role == "Whereby Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WherebyAgent()
        result = agent.execute("test task")
        assert "Whereby Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WherebyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WherebyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_862"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert whereby_agent.agent_id == "agent_862"


class TestWherebyIntegration:
    """Integration tests for Whereby Agent"""

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