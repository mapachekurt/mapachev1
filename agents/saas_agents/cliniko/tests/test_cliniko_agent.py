"""
Tests for Cliniko Agent
"""

import pytest
from agents.saas_agents.cliniko.agent import ClinikoAgent, cliniko_agent


class TestClinikoAgent:
    """Test suite for Cliniko Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ClinikoAgent()
        assert agent.agent_id == "agent_1031"
        assert agent.role == "Cliniko Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ClinikoAgent()
        result = agent.execute("test task")
        assert "Cliniko Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ClinikoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ClinikoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1031"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cliniko_agent.agent_id == "agent_1031"


class TestClinikoIntegration:
    """Integration tests for Cliniko Agent"""

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