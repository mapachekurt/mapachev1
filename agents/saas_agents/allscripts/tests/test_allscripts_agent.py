"""
Tests for Allscripts Agent
"""

import pytest
from agents.saas_agents.allscripts.agent import AllscriptsAgent, allscripts_agent


class TestAllscriptsAgent:
    """Test suite for Allscripts Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AllscriptsAgent()
        assert agent.agent_id == "agent_1015"
        assert agent.role == "Allscripts Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AllscriptsAgent()
        result = agent.execute("test task")
        assert "Allscripts Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AllscriptsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AllscriptsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1015"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert allscripts_agent.agent_id == "agent_1015"


class TestAllscriptsIntegration:
    """Integration tests for Allscripts Agent"""

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