"""
Tests for Microsoft SharePoint Agent
"""

import pytest
from agents.saas_agents.sharepoint.agent import SharepointAgent, sharepoint_agent


class TestSharepointAgent:
    """Test suite for Microsoft SharePoint Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SharepointAgent()
        assert agent.agent_id == "agent_523"
        assert agent.role == "Microsoft SharePoint Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "collaboration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SharepointAgent()
        result = agent.execute("test task")
        assert "Microsoft SharePoint Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SharepointAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SharepointAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_523"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "collaboration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sharepoint_agent.agent_id == "agent_523"


class TestSharepointIntegration:
    """Integration tests for Microsoft SharePoint Agent"""

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