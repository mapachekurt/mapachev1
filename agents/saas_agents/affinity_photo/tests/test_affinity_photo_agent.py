"""
Tests for Affinity Photo Agent
"""

import pytest
from agents.saas_agents.affinity_photo.agent import AffinityPhotoAgent, affinity_photo_agent


class TestAffinityPhotoAgent:
    """Test suite for Affinity Photo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AffinityPhotoAgent()
        assert agent.agent_id == "agent_770"
        assert agent.role == "Affinity Photo Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "design"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AffinityPhotoAgent()
        result = agent.execute("test task")
        assert "Affinity Photo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AffinityPhotoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AffinityPhotoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_770"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "design"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert affinity_photo_agent.agent_id == "agent_770"


class TestAffinityPhotoIntegration:
    """Integration tests for Affinity Photo Agent"""

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