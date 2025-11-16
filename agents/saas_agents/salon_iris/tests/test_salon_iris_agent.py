"""
Tests for Salon Iris Agent
"""

import pytest
from agents.saas_agents.salon_iris.agent import SalonIrisAgent, salon_iris_agent


class TestSalonIrisAgent:
    """Test suite for Salon Iris Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SalonIrisAgent()
        assert agent.agent_id == "agent_1207"
        assert agent.role == "Salon Iris Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SalonIrisAgent()
        result = agent.execute("test task")
        assert "Salon Iris Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SalonIrisAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SalonIrisAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1207"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert salon_iris_agent.agent_id == "agent_1207"


class TestSalonIrisIntegration:
    """Integration tests for Salon Iris Agent"""

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