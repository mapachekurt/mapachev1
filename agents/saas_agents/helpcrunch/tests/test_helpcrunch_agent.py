"""
Tests for HelpCrunch Agent
"""

import pytest
from agents.saas_agents.helpcrunch.agent import HelpcrunchAgent, helpcrunch_agent


class TestHelpcrunchAgent:
    """Test suite for HelpCrunch Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HelpcrunchAgent()
        assert agent.agent_id == "agent_1004"
        assert agent.role == "HelpCrunch Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HelpcrunchAgent()
        result = agent.execute("test task")
        assert "HelpCrunch Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HelpcrunchAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HelpcrunchAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1004"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert helpcrunch_agent.agent_id == "agent_1004"


class TestHelpcrunchIntegration:
    """Integration tests for HelpCrunch Agent"""

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