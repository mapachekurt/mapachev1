"""
Tests for Zenefits Agent
"""

import pytest
from agents.saas_agents.zenefits.agent import ZenefitsAgent, zenefits_agent


class TestZenefitsAgent:
    """Test suite for Zenefits Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZenefitsAgent()
        assert agent.agent_id == "agent_958"
        assert agent.role == "Zenefits Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZenefitsAgent()
        result = agent.execute("test task")
        assert "Zenefits Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZenefitsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZenefitsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_958"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zenefits_agent.agent_id == "agent_958"


class TestZenefitsIntegration:
    """Integration tests for Zenefits Agent"""

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