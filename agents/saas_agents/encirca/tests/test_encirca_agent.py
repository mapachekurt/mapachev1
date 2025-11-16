"""
Tests for Encirca Agent
"""

import pytest
from agents.saas_agents.encirca.agent import EncircaAgent, encirca_agent


class TestEncircaAgent:
    """Test suite for Encirca Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = EncircaAgent()
        assert agent.agent_id == "agent_1289"
        assert agent.role == "Encirca Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "agriculture"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = EncircaAgent()
        result = agent.execute("test task")
        assert "Encirca Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = EncircaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = EncircaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1289"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "agriculture"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert encirca_agent.agent_id == "agent_1289"


class TestEncircaIntegration:
    """Integration tests for Encirca Agent"""

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