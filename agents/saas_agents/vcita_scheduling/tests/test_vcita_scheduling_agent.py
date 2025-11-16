"""
Tests for vcita Scheduling Agent
"""

import pytest
from agents.saas_agents.vcita_scheduling.agent import VcitaSchedulingAgent, vcita_scheduling_agent


class TestVcitaSchedulingAgent:
    """Test suite for vcita Scheduling Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VcitaSchedulingAgent()
        assert agent.agent_id == "agent_855"
        assert agent.role == "vcita Scheduling Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VcitaSchedulingAgent()
        result = agent.execute("test task")
        assert "vcita Scheduling Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VcitaSchedulingAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VcitaSchedulingAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_855"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert vcita_scheduling_agent.agent_id == "agent_855"


class TestVcitaSchedulingIntegration:
    """Integration tests for vcita Scheduling Agent"""

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