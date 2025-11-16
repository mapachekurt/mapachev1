"""
Tests for Drip Agent
"""

import pytest
from agents.saas_agents.drip.agent import DripAgent, drip_agent


class TestDripAgent:
    """Test suite for Drip Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DripAgent()
        assert agent.agent_id == "agent_587"
        assert agent.role == "Drip Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "marketing_automation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DripAgent()
        result = agent.execute("test task")
        assert "Drip Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DripAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DripAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_587"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "marketing_automation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert drip_agent.agent_id == "agent_587"


class TestDripIntegration:
    """Integration tests for Drip Agent"""

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