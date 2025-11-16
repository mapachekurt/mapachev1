"""
Tests for Seafile Agent
"""

import pytest
from agents.saas_agents.seafile.agent import SeafileAgent, seafile_agent


class TestSeafileAgent:
    """Test suite for Seafile Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SeafileAgent()
        assert agent.agent_id == "agent_793"
        assert agent.role == "Seafile Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "file_sharing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SeafileAgent()
        result = agent.execute("test task")
        assert "Seafile Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SeafileAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SeafileAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_793"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "file_sharing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert seafile_agent.agent_id == "agent_793"


class TestSeafileIntegration:
    """Integration tests for Seafile Agent"""

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