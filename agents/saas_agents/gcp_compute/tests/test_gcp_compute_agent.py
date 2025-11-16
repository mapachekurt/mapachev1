"""
Tests for GCP Compute Engine Agent
"""

import pytest
from agents.saas_agents.gcp_compute.agent import GcpComputeAgent, gcp_compute_agent


class TestGcpComputeAgent:
    """Test suite for GCP Compute Engine Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GcpComputeAgent()
        assert agent.agent_id == "agent_662"
        assert agent.role == "GCP Compute Engine Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GcpComputeAgent()
        result = agent.execute("test task")
        assert "GCP Compute Engine Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GcpComputeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GcpComputeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_662"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gcp_compute_agent.agent_id == "agent_662"


class TestGcpComputeIntegration:
    """Integration tests for GCP Compute Engine Agent"""

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