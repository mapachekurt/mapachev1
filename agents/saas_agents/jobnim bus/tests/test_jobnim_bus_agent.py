"""
Tests for Jobnim bus Agent
"""

import pytest
from agents.saas_agents.jobnim bus.agent import JobnimBusAgent, jobnim_bus_agent


class TestJobnimBusAgent:
    """Test suite for Jobnim bus Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JobnimBusAgent()
        assert agent.agent_id == "agent_1106"
        assert agent.role == "Jobnim bus Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JobnimBusAgent()
        result = agent.execute("test task")
        assert "Jobnim bus Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JobnimBusAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JobnimBusAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1106"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert jobnim_bus_agent.agent_id == "agent_1106"


class TestJobnimBusIntegration:
    """Integration tests for Jobnim bus Agent"""

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