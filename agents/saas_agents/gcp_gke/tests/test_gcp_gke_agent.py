"""
Tests for GCP GKE Agent
"""

import pytest
from agents.saas_agents.gcp_gke.agent import GcpGkeAgent, gcp_gke_agent


class TestGcpGkeAgent:
    """Test suite for GCP GKE Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GcpGkeAgent()
        assert agent.agent_id == "agent_670"
        assert agent.role == "GCP GKE Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GcpGkeAgent()
        result = agent.execute("test task")
        assert "GCP GKE Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GcpGkeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GcpGkeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_670"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gcp_gke_agent.agent_id == "agent_670"


class TestGcpGkeIntegration:
    """Integration tests for GCP GKE Agent"""

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