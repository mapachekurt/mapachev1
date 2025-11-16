"""
Tests for Acumatica Agent
"""

import pytest
from agents.saas_agents.acumatica.agent import AcumaticaAgent, acumatica_agent


class TestAcumaticaAgent:
    """Test suite for Acumatica Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AcumaticaAgent()
        assert agent.agent_id == "agent_1310"
        assert agent.role == "Acumatica Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "manufacturing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AcumaticaAgent()
        result = agent.execute("test task")
        assert "Acumatica Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AcumaticaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AcumaticaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1310"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "manufacturing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert acumatica_agent.agent_id == "agent_1310"


class TestAcumaticaIntegration:
    """Integration tests for Acumatica Agent"""

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