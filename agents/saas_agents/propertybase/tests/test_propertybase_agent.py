"""
Tests for Propertybase Agent
"""

import pytest
from agents.saas_agents.propertybase.agent import PropertybaseAgent, propertybase_agent


class TestPropertybaseAgent:
    """Test suite for Propertybase Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PropertybaseAgent()
        assert agent.agent_id == "agent_1076"
        assert agent.role == "Propertybase Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PropertybaseAgent()
        result = agent.execute("test task")
        assert "Propertybase Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PropertybaseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PropertybaseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1076"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert propertybase_agent.agent_id == "agent_1076"


class TestPropertybaseIntegration:
    """Integration tests for Propertybase Agent"""

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