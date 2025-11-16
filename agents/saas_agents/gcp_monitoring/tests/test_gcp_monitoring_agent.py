"""
Tests for GCP Cloud Monitoring Agent
"""

import pytest
from agents.saas_agents.gcp_monitoring.agent import GcpMonitoringAgent, gcp_monitoring_agent


class TestGcpMonitoringAgent:
    """Test suite for GCP Cloud Monitoring Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GcpMonitoringAgent()
        assert agent.agent_id == "agent_671"
        assert agent.role == "GCP Cloud Monitoring Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GcpMonitoringAgent()
        result = agent.execute("test task")
        assert "GCP Cloud Monitoring Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GcpMonitoringAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GcpMonitoringAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_671"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gcp_monitoring_agent.agent_id == "agent_671"


class TestGcpMonitoringIntegration:
    """Integration tests for GCP Cloud Monitoring Agent"""

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