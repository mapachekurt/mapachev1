"""
Tests for ServiceTitan Agent
"""

import pytest
from agents.saas_agents.service_titan.agent import ServiceTitanAgent, service_titan_agent


class TestServiceTitanAgent:
    """Test suite for ServiceTitan Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ServiceTitanAgent()
        assert agent.agent_id == "agent_1103"
        assert agent.role == "ServiceTitan Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ServiceTitanAgent()
        result = agent.execute("test task")
        assert "ServiceTitan Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ServiceTitanAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ServiceTitanAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1103"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert service_titan_agent.agent_id == "agent_1103"


class TestServiceTitanIntegration:
    """Integration tests for ServiceTitan Agent"""

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