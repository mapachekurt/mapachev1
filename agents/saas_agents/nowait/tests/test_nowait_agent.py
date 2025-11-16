"""
Tests for Nowait Agent
"""

import pytest
from agents.saas_agents.nowait.agent import NowaitAgent, nowait_agent


class TestNowaitAgent:
    """Test suite for Nowait Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NowaitAgent()
        assert agent.agent_id == "agent_1197"
        assert agent.role == "Nowait Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NowaitAgent()
        result = agent.execute("test task")
        assert "Nowait Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NowaitAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NowaitAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1197"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nowait_agent.agent_id == "agent_1197"


class TestNowaitIntegration:
    """Integration tests for Nowait Agent"""

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