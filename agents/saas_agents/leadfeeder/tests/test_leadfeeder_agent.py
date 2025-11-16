"""
Tests for Leadfeeder Agent
"""

import pytest
from agents.saas_agents.leadfeeder.agent import LeadfeederAgent, leadfeeder_agent


class TestLeadfeederAgent:
    """Test suite for Leadfeeder Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LeadfeederAgent()
        assert agent.agent_id == "agent_612"
        assert agent.role == "Leadfeeder Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LeadfeederAgent()
        result = agent.execute("test task")
        assert "Leadfeeder Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LeadfeederAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LeadfeederAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_612"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert leadfeeder_agent.agent_id == "agent_612"


class TestLeadfeederIntegration:
    """Integration tests for Leadfeeder Agent"""

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