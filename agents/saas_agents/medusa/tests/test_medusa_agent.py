"""
Tests for Medusa Agent
"""

import pytest
from agents.saas_agents.medusa.agent import MedusaAgent, medusa_agent


class TestMedusaAgent:
    """Test suite for Medusa Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MedusaAgent()
        assert agent.agent_id == "agent_981"
        assert agent.role == "Medusa Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MedusaAgent()
        result = agent.execute("test task")
        assert "Medusa Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MedusaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MedusaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_981"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert medusa_agent.agent_id == "agent_981"


class TestMedusaIntegration:
    """Integration tests for Medusa Agent"""

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