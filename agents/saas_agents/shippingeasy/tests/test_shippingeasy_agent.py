"""
Tests for ShippingEasy Agent
"""

import pytest
from agents.saas_agents.shippingeasy.agent import ShippingeasyAgent, shippingeasy_agent


class TestShippingeasyAgent:
    """Test suite for ShippingEasy Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ShippingeasyAgent()
        assert agent.agent_id == "agent_1120"
        assert agent.role == "ShippingEasy Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "logistics"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ShippingeasyAgent()
        result = agent.execute("test task")
        assert "ShippingEasy Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ShippingeasyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ShippingeasyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1120"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "logistics"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert shippingeasy_agent.agent_id == "agent_1120"


class TestShippingeasyIntegration:
    """Integration tests for ShippingEasy Agent"""

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