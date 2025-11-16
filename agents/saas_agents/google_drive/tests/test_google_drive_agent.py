"""
Tests for Google Drive Agent
"""

import pytest
from agents.saas_agents.google_drive.agent import GoogleDriveAgent, google_drive_agent


class TestGoogleDriveAgent:
    """Test suite for Google Drive Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GoogleDriveAgent()
        assert agent.agent_id == "agent_518"
        assert agent.role == "Google Drive Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "storage"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GoogleDriveAgent()
        result = agent.execute("test task")
        assert "Google Drive Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GoogleDriveAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GoogleDriveAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_518"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "storage"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert google_drive_agent.agent_id == "agent_518"


class TestGoogleDriveIntegration:
    """Integration tests for Google Drive Agent"""

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