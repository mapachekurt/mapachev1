"""
Tests for Vanta Agent
"""

import pytest
from agents.saas_agents.vanta.agent import VantaAgent, vanta_agent


class TestVantaAgent:
    """Test suite for Vanta Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VantaAgent()
        assert agent.agent_id == "agent_1445"
        assert agent.role == "Vanta Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "compliance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VantaAgent()
        result = agent.execute("test task")
        assert "Vanta Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VantaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VantaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1445"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "compliance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert vanta_agent.agent_id == "agent_1445"


class TestVantaIntegration:
    """Integration tests for Vanta Agent"""

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