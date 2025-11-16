"""
Tests for Hyperproof Agent
"""

import pytest
from agents.saas_agents.hyperproof.agent import HyperproofAgent, hyperproof_agent


class TestHyperproofAgent:
    """Test suite for Hyperproof Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HyperproofAgent()
        assert agent.agent_id == "agent_1450"
        assert agent.role == "Hyperproof Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "compliance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HyperproofAgent()
        result = agent.execute("test task")
        assert "Hyperproof Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HyperproofAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HyperproofAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1450"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "compliance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hyperproof_agent.agent_id == "agent_1450"


class TestHyperproofIntegration:
    """Integration tests for Hyperproof Agent"""

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