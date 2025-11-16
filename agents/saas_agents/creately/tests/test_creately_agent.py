"""
Tests for Creately Agent
"""

import pytest
from agents.saas_agents.creately.agent import CreatelyAgent, creately_agent


class TestCreatelyAgent:
    """Test suite for Creately Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CreatelyAgent()
        assert agent.agent_id == "agent_1337"
        assert agent.role == "Creately Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "collaboration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CreatelyAgent()
        result = agent.execute("test task")
        assert "Creately Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CreatelyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CreatelyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1337"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "collaboration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert creately_agent.agent_id == "agent_1337"


class TestCreatelyIntegration:
    """Integration tests for Creately Agent"""

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