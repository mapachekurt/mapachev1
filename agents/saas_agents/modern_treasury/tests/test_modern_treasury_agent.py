"""
Tests for Modern Treasury Agent
"""

import pytest
from agents.saas_agents.modern_treasury.agent import ModernTreasuryAgent, modern_treasury_agent


class TestModernTreasuryAgent:
    """Test suite for Modern Treasury Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ModernTreasuryAgent()
        assert agent.agent_id == "agent_1510"
        assert agent.role == "Modern Treasury Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ModernTreasuryAgent()
        result = agent.execute("test task")
        assert "Modern Treasury Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ModernTreasuryAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ModernTreasuryAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1510"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert modern_treasury_agent.agent_id == "agent_1510"


class TestModernTreasuryIntegration:
    """Integration tests for Modern Treasury Agent"""

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