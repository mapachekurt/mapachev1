"""
Tests for Maitre'D Agent
"""

import pytest
from agents.saas_agents.maitre_d.agent import MaitreDAgent, maitre_d_agent


class TestMaitreDAgent:
    """Test suite for Maitre'D Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MaitreDAgent()
        assert agent.agent_id == "agent_1162"
        assert agent.role == "Maitre'D Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MaitreDAgent()
        result = agent.execute("test task")
        assert "Maitre'D Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MaitreDAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MaitreDAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1162"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert maitre_d_agent.agent_id == "agent_1162"


class TestMaitreDIntegration:
    """Integration tests for Maitre'D Agent"""

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