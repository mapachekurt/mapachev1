"""
Tests for Linode Object Storage Agent
"""

import pytest
from agents.saas_agents.linode_object_storage.agent import LinodeObjectStorageAgent, linode_object_storage_agent


class TestLinodeObjectStorageAgent:
    """Test suite for Linode Object Storage Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LinodeObjectStorageAgent()
        assert agent.agent_id == "agent_800"
        assert agent.role == "Linode Object Storage Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "file_sharing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LinodeObjectStorageAgent()
        result = agent.execute("test task")
        assert "Linode Object Storage Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LinodeObjectStorageAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LinodeObjectStorageAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_800"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "file_sharing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert linode_object_storage_agent.agent_id == "agent_800"


class TestLinodeObjectStorageIntegration:
    """Integration tests for Linode Object Storage Agent"""

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