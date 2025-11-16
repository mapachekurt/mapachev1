"""
Tests for BlazeMeter Agent
"""

import pytest
from agents.saas_agents.blazemeter.agent import BlazemeterAgent, blazemeter_agent


class TestBlazemeterAgent:
    """Test suite for BlazeMeter Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BlazemeterAgent()
        assert agent.agent_id == "agent_1402"
        assert agent.role == "BlazeMeter Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BlazemeterAgent()
        result = agent.execute("test task")
        assert "BlazeMeter Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BlazemeterAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BlazemeterAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1402"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert blazemeter_agent.agent_id == "agent_1402"


class TestBlazemeterIntegration:
    """Integration tests for BlazeMeter Agent"""

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