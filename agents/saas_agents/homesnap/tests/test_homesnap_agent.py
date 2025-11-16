"""
Tests for Homesnap Agent
"""

import pytest
from agents.saas_agents.homesnap.agent import HomesnapAgent, homesnap_agent


class TestHomesnapAgent:
    """Test suite for Homesnap Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HomesnapAgent()
        assert agent.agent_id == "agent_1091"
        assert agent.role == "Homesnap Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HomesnapAgent()
        result = agent.execute("test task")
        assert "Homesnap Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HomesnapAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HomesnapAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1091"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert homesnap_agent.agent_id == "agent_1091"


class TestHomesnapIntegration:
    """Integration tests for Homesnap Agent"""

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