"""
Tests for GCP Cloud Storage Agent
"""

import pytest
from agents.saas_agents.gcp_storage.agent import GcpStorageAgent, gcp_storage_agent


class TestGcpStorageAgent:
    """Test suite for GCP Cloud Storage Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GcpStorageAgent()
        assert agent.agent_id == "agent_663"
        assert agent.role == "GCP Cloud Storage Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GcpStorageAgent()
        result = agent.execute("test task")
        assert "GCP Cloud Storage Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GcpStorageAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GcpStorageAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_663"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gcp_storage_agent.agent_id == "agent_663"


class TestGcpStorageIntegration:
    """Integration tests for GCP Cloud Storage Agent"""

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