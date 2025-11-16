"""
Tests for Microsoft OneNote Agent
"""

import pytest
from agents.saas_agents.onenote.agent import OnenoteAgent, onenote_agent


class TestOnenoteAgent:
    """Test suite for Microsoft OneNote Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OnenoteAgent()
        assert agent.agent_id == "agent_743"
        assert agent.role == "Microsoft OneNote Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "notes"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OnenoteAgent()
        result = agent.execute("test task")
        assert "Microsoft OneNote Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OnenoteAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OnenoteAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_743"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "notes"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert onenote_agent.agent_id == "agent_743"


class TestOnenoteIntegration:
    """Integration tests for Microsoft OneNote Agent"""

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