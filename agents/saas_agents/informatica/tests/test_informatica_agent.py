"""
Tests for Informatica Agent
"""

import pytest
from agents.saas_agents.informatica.agent import InformaticaAgent, informatica_agent


class TestInformaticaAgent:
    """Test suite for Informatica Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = InformaticaAgent()
        assert agent.agent_id == "agent_1376"
        assert agent.role == "Informatica Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "data"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = InformaticaAgent()
        result = agent.execute("test task")
        assert "Informatica Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = InformaticaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = InformaticaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1376"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "data"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert informatica_agent.agent_id == "agent_1376"


class TestInformaticaIntegration:
    """Integration tests for Informatica Agent"""

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