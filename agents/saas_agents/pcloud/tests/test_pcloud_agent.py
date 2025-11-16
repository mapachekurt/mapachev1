"""
Tests for pCloud Agent
"""

import pytest
from agents.saas_agents.pcloud.agent import PcloudAgent, pcloud_agent


class TestPcloudAgent:
    """Test suite for pCloud Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PcloudAgent()
        assert agent.agent_id == "agent_794"
        assert agent.role == "pCloud Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "file_sharing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PcloudAgent()
        result = agent.execute("test task")
        assert "pCloud Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PcloudAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PcloudAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_794"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "file_sharing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pcloud_agent.agent_id == "agent_794"


class TestPcloudIntegration:
    """Integration tests for pCloud Agent"""

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