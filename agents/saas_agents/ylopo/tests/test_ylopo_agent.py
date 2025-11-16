"""
Tests for Ylopo Agent
"""

import pytest
from agents.saas_agents.ylopo.agent import YlopoAgent, ylopo_agent


class TestYlopoAgent:
    """Test suite for Ylopo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = YlopoAgent()
        assert agent.agent_id == "agent_1088"
        assert agent.role == "Ylopo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = YlopoAgent()
        result = agent.execute("test task")
        assert "Ylopo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = YlopoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = YlopoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1088"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ylopo_agent.agent_id == "agent_1088"


class TestYlopoIntegration:
    """Integration tests for Ylopo Agent"""

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