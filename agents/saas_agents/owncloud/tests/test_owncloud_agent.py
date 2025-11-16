"""
Tests for ownCloud Agent
"""

import pytest
from agents.saas_agents.owncloud.agent import OwncloudAgent, owncloud_agent


class TestOwncloudAgent:
    """Test suite for ownCloud Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OwncloudAgent()
        assert agent.agent_id == "agent_792"
        assert agent.role == "ownCloud Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "file_sharing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OwncloudAgent()
        result = agent.execute("test task")
        assert "ownCloud Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OwncloudAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OwncloudAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_792"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "file_sharing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert owncloud_agent.agent_id == "agent_792"


class TestOwncloudIntegration:
    """Integration tests for ownCloud Agent"""

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