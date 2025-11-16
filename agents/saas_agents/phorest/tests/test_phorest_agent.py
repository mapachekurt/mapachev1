"""
Tests for Phorest Agent
"""

import pytest
from agents.saas_agents.phorest.agent import PhorestAgent, phorest_agent


class TestPhorestAgent:
    """Test suite for Phorest Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PhorestAgent()
        assert agent.agent_id == "agent_1205"
        assert agent.role == "Phorest Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PhorestAgent()
        result = agent.execute("test task")
        assert "Phorest Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PhorestAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PhorestAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1205"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert phorest_agent.agent_id == "agent_1205"


class TestPhorestIntegration:
    """Integration tests for Phorest Agent"""

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