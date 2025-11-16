"""
Tests for Qudini Agent
"""

import pytest
from agents.saas_agents.qudini.agent import QudiniAgent, qudini_agent


class TestQudiniAgent:
    """Test suite for Qudini Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = QudiniAgent()
        assert agent.agent_id == "agent_1199"
        assert agent.role == "Qudini Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = QudiniAgent()
        result = agent.execute("test task")
        assert "Qudini Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = QudiniAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = QudiniAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1199"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert qudini_agent.agent_id == "agent_1199"


class TestQudiniIntegration:
    """Integration tests for Qudini Agent"""

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