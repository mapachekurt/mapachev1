"""
Tests for Demio Agent
"""

import pytest
from agents.saas_agents.demio.agent import DemioAgent, demio_agent


class TestDemioAgent:
    """Test suite for Demio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DemioAgent()
        assert agent.agent_id == "agent_875"
        assert agent.role == "Demio Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "video"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DemioAgent()
        result = agent.execute("test task")
        assert "Demio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DemioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DemioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_875"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "video"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert demio_agent.agent_id == "agent_875"


class TestDemioIntegration:
    """Integration tests for Demio Agent"""

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