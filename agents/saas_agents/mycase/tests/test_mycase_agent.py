"""
Tests for MyCase Agent
"""

import pytest
from agents.saas_agents.mycase.agent import MycaseAgent, mycase_agent


class TestMycaseAgent:
    """Test suite for MyCase Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MycaseAgent()
        assert agent.agent_id == "agent_1033"
        assert agent.role == "MyCase Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MycaseAgent()
        result = agent.execute("test task")
        assert "MyCase Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MycaseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MycaseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1033"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mycase_agent.agent_id == "agent_1033"


class TestMycaseIntegration:
    """Integration tests for MyCase Agent"""

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