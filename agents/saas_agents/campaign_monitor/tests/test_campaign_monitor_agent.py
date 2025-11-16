"""
Tests for Campaign Monitor Agent
"""

import pytest
from agents.saas_agents.campaign_monitor.agent import CampaignMonitorAgent, campaign_monitor_agent


class TestCampaignMonitorAgent:
    """Test suite for Campaign Monitor Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CampaignMonitorAgent()
        assert agent.agent_id == "agent_534"
        assert agent.role == "Campaign Monitor Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CampaignMonitorAgent()
        result = agent.execute("test task")
        assert "Campaign Monitor Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CampaignMonitorAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CampaignMonitorAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_534"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert campaign_monitor_agent.agent_id == "agent_534"


class TestCampaignMonitorIntegration:
    """Integration tests for Campaign Monitor Agent"""

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