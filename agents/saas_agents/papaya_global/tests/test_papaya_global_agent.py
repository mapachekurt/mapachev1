"""
Tests for Papaya Global Agent
"""

import pytest
from agents.saas_agents.papaya_global.agent import PapayaGlobalAgent, papaya_global_agent


class TestPapayaGlobalAgent:
    """Test suite for Papaya Global Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PapayaGlobalAgent()
        assert agent.agent_id == "agent_963"
        assert agent.role == "Papaya Global Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PapayaGlobalAgent()
        result = agent.execute("test task")
        assert "Papaya Global Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PapayaGlobalAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PapayaGlobalAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_963"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert papaya_global_agent.agent_id == "agent_963"


class TestPapayaGlobalIntegration:
    """Integration tests for Papaya Global Agent"""

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