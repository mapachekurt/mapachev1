"""
Tests for LeadIQ Agent
"""

import pytest
from agents.saas_agents.leadiq.agent import LeadiqAgent, leadiq_agent


class TestLeadiqAgent:
    """Test suite for LeadIQ Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LeadiqAgent()
        assert agent.agent_id == "agent_620"
        assert agent.role == "LeadIQ Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LeadiqAgent()
        result = agent.execute("test task")
        assert "LeadIQ Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LeadiqAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LeadiqAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_620"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert leadiq_agent.agent_id == "agent_620"


class TestLeadiqIntegration:
    """Integration tests for LeadIQ Agent"""

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