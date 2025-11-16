"""
Tests for Redfin Agent
"""

import pytest
from agents.saas_agents.redfin.agent import RedfinAgent, redfin_agent


class TestRedfinAgent:
    """Test suite for Redfin Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RedfinAgent()
        assert agent.agent_id == "agent_1074"
        assert agent.role == "Redfin Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RedfinAgent()
        result = agent.execute("test task")
        assert "Redfin Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RedfinAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RedfinAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1074"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert redfin_agent.agent_id == "agent_1074"


class TestRedfinIntegration:
    """Integration tests for Redfin Agent"""

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