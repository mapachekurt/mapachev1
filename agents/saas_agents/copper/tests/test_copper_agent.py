"""
Tests for Copper CRM Agent
"""

import pytest
from agents.saas_agents.copper.agent import CopperAgent, copper_agent


class TestCopperAgent:
    """Test suite for Copper CRM Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CopperAgent()
        assert agent.agent_id == "agent_573"
        assert agent.role == "Copper CRM Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CopperAgent()
        result = agent.execute("test task")
        assert "Copper CRM Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CopperAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CopperAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_573"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert copper_agent.agent_id == "agent_573"


class TestCopperIntegration:
    """Integration tests for Copper CRM Agent"""

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