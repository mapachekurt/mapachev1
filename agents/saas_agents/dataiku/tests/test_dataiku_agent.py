"""
Tests for Dataiku Agent
"""

import pytest
from agents.saas_agents.dataiku.agent import DataikuAgent, dataiku_agent


class TestDataikuAgent:
    """Test suite for Dataiku Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DataikuAgent()
        assert agent.agent_id == "agent_1412"
        assert agent.role == "Dataiku Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DataikuAgent()
        result = agent.execute("test task")
        assert "Dataiku Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DataikuAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DataikuAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1412"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dataiku_agent.agent_id == "agent_1412"


class TestDataikuIntegration:
    """Integration tests for Dataiku Agent"""

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