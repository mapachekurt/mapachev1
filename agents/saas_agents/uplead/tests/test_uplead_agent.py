"""
Tests for UpLead Agent
"""

import pytest
from agents.saas_agents.uplead.agent import UpleadAgent, uplead_agent


class TestUpleadAgent:
    """Test suite for UpLead Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = UpleadAgent()
        assert agent.agent_id == "agent_621"
        assert agent.role == "UpLead Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = UpleadAgent()
        result = agent.execute("test task")
        assert "UpLead Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = UpleadAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = UpleadAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_621"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert uplead_agent.agent_id == "agent_621"


class TestUpleadIntegration:
    """Integration tests for UpLead Agent"""

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