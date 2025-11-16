"""
Tests for JotForm Agent
"""

import pytest
from agents.saas_agents.jotform.agent import JotformAgent, jotform_agent


class TestJotformAgent:
    """Test suite for JotForm Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JotformAgent()
        assert agent.agent_id == "agent_880"
        assert agent.role == "JotForm Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JotformAgent()
        result = agent.execute("test task")
        assert "JotForm Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JotformAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JotformAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_880"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert jotform_agent.agent_id == "agent_880"


class TestJotformIntegration:
    """Integration tests for JotForm Agent"""

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