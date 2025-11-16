"""
Tests for Kustomer Agent
"""

import pytest
from agents.saas_agents.kustomer.agent import KustomerAgent, kustomer_agent


class TestKustomerAgent:
    """Test suite for Kustomer Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KustomerAgent()
        assert agent.agent_id == "agent_1006"
        assert agent.role == "Kustomer Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KustomerAgent()
        result = agent.execute("test task")
        assert "Kustomer Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KustomerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KustomerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1006"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kustomer_agent.agent_id == "agent_1006"


class TestKustomerIntegration:
    """Integration tests for Kustomer Agent"""

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