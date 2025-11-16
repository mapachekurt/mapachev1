"""
Tests for PCLaw Agent
"""

import pytest
from agents.saas_agents.pclaw.agent import PclawAgent, pclaw_agent


class TestPclawAgent:
    """Test suite for PCLaw Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PclawAgent()
        assert agent.agent_id == "agent_1049"
        assert agent.role == "PCLaw Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PclawAgent()
        result = agent.execute("test task")
        assert "PCLaw Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PclawAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PclawAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1049"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pclaw_agent.agent_id == "agent_1049"


class TestPclawIntegration:
    """Integration tests for PCLaw Agent"""

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