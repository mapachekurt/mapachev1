"""
Tests for Prometheus Agent
"""

import pytest
from agents.saas_agents.prometheus.agent import PrometheusAgent, prometheus_agent


class TestPrometheusAgent:
    """Test suite for Prometheus Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PrometheusAgent()
        assert agent.agent_id == "agent_672"
        assert agent.role == "Prometheus Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "monitoring"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PrometheusAgent()
        result = agent.execute("test task")
        assert "Prometheus Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PrometheusAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PrometheusAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_672"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "monitoring"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert prometheus_agent.agent_id == "agent_672"


class TestPrometheusIntegration:
    """Integration tests for Prometheus Agent"""

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