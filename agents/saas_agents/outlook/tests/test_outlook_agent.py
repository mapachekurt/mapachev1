"""
Tests for Microsoft Outlook Agent
"""

import pytest
from agents.saas_agents.outlook.agent import OutlookAgent, outlook_agent


class TestOutlookAgent:
    """Test suite for Microsoft Outlook Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = OutlookAgent()
        assert agent.agent_id == "agent_521"
        assert agent.role == "Microsoft Outlook Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "email"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = OutlookAgent()
        result = agent.execute("test task")
        assert "Microsoft Outlook Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = OutlookAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = OutlookAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_521"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "email"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert outlook_agent.agent_id == "agent_521"


class TestOutlookIntegration:
    """Integration tests for Microsoft Outlook Agent"""

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