"""
Tests for Microsoft OneDrive Agent
"""

import pytest
from agents.saas_agents.onedrive.agent import OnedriveAgent, onedrive_agent


class TestOnedriveAgent:
    """Test suite for Microsoft OneDrive Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OnedriveAgent()
        assert agent.agent_id == "agent_522"
        assert agent.role == "Microsoft OneDrive Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "storage"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OnedriveAgent()
        result = agent.execute("test task")
        assert "Microsoft OneDrive Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OnedriveAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OnedriveAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_522"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "storage"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert onedrive_agent.agent_id == "agent_522"


class TestOnedriveIntegration:
    """Integration tests for Microsoft OneDrive Agent"""

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