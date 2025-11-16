"""
Tests for Erply Agent
"""

import pytest
from agents.saas_agents.erply.agent import ErplyAgent, erply_agent


class TestErplyAgent:
    """Test suite for Erply Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ErplyAgent()
        assert agent.agent_id == "agent_1176"
        assert agent.role == "Erply Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ErplyAgent()
        result = agent.execute("test task")
        assert "Erply Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ErplyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ErplyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1176"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert erply_agent.agent_id == "agent_1176"


class TestErplyIntegration:
    """Integration tests for Erply Agent"""

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