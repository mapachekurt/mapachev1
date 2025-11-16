"""
Tests for WhiteSource Agent
"""

import pytest
from agents.saas_agents.whitesource.agent import WhitesourceAgent, whitesource_agent


class TestWhitesourceAgent:
    """Test suite for WhiteSource Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WhitesourceAgent()
        assert agent.agent_id == "agent_719"
        assert agent.role == "WhiteSource Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "code_quality"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WhitesourceAgent()
        result = agent.execute("test task")
        assert "WhiteSource Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WhitesourceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WhitesourceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_719"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "code_quality"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert whitesource_agent.agent_id == "agent_719"


class TestWhitesourceIntegration:
    """Integration tests for WhiteSource Agent"""

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