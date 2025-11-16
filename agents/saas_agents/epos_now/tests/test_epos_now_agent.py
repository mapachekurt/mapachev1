"""
Tests for Epos Now Agent
"""

import pytest
from agents.saas_agents.epos_now.agent import EposNowAgent, epos_now_agent


class TestEposNowAgent:
    """Test suite for Epos Now Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = EposNowAgent()
        assert agent.agent_id == "agent_1170"
        assert agent.role == "Epos Now Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = EposNowAgent()
        result = agent.execute("test task")
        assert "Epos Now Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = EposNowAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = EposNowAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1170"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert epos_now_agent.agent_id == "agent_1170"


class TestEposNowIntegration:
    """Integration tests for Epos Now Agent"""

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