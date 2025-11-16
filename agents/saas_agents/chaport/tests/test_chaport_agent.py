"""
Tests for Chaport Agent
"""

import pytest
from agents.saas_agents.chaport.agent import ChaportAgent, chaport_agent


class TestChaportAgent:
    """Test suite for Chaport Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ChaportAgent()
        assert agent.agent_id == "agent_1003"
        assert agent.role == "Chaport Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ChaportAgent()
        result = agent.execute("test task")
        assert "Chaport Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ChaportAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ChaportAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1003"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert chaport_agent.agent_id == "agent_1003"


class TestChaportIntegration:
    """Integration tests for Chaport Agent"""

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