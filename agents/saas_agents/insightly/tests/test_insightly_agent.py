"""
Tests for Insightly Agent
"""

import pytest
from agents.saas_agents.insightly.agent import InsightlyAgent, insightly_agent


class TestInsightlyAgent:
    """Test suite for Insightly Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = InsightlyAgent()
        assert agent.agent_id == "agent_575"
        assert agent.role == "Insightly Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = InsightlyAgent()
        result = agent.execute("test task")
        assert "Insightly Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = InsightlyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = InsightlyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_575"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert insightly_agent.agent_id == "agent_575"


class TestInsightlyIntegration:
    """Integration tests for Insightly Agent"""

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