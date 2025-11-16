"""
Tests for Ayoa Agent
"""

import pytest
from agents.saas_agents.ayoa.agent import AyoaAgent, ayoa_agent


class TestAyoaAgent:
    """Test suite for Ayoa Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AyoaAgent()
        assert agent.agent_id == "agent_1351"
        assert agent.role == "Ayoa Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "collaboration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AyoaAgent()
        result = agent.execute("test task")
        assert "Ayoa Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AyoaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AyoaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1351"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "collaboration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ayoa_agent.agent_id == "agent_1351"


class TestAyoaIntegration:
    """Integration tests for Ayoa Agent"""

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