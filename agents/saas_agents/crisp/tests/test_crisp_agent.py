"""
Tests for Crisp Agent
"""

import pytest
from agents.saas_agents.crisp.agent import CrispAgent, crisp_agent


class TestCrispAgent:
    """Test suite for Crisp Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CrispAgent()
        assert agent.agent_id == "agent_993"
        assert agent.role == "Crisp Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CrispAgent()
        result = agent.execute("test task")
        assert "Crisp Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CrispAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CrispAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_993"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert crisp_agent.agent_id == "agent_993"


class TestCrispIntegration:
    """Integration tests for Crisp Agent"""

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