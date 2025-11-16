"""
Tests for Bamboo Agent
"""

import pytest
from agents.saas_agents.bamboo.agent import BambooAgent, bamboo_agent


class TestBambooAgent:
    """Test suite for Bamboo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BambooAgent()
        assert agent.agent_id == "agent_627"
        assert agent.role == "Bamboo Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "ci_cd"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BambooAgent()
        result = agent.execute("test task")
        assert "Bamboo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BambooAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BambooAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_627"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "ci_cd"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bamboo_agent.agent_id == "agent_627"


class TestBambooIntegration:
    """Integration tests for Bamboo Agent"""

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