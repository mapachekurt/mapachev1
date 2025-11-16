"""
Tests for Wufoo Agent
"""

import pytest
from agents.saas_agents.wufoo.agent import WufooAgent, wufoo_agent


class TestWufooAgent:
    """Test suite for Wufoo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WufooAgent()
        assert agent.agent_id == "agent_882"
        assert agent.role == "Wufoo Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WufooAgent()
        result = agent.execute("test task")
        assert "Wufoo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WufooAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WufooAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_882"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wufoo_agent.agent_id == "agent_882"


class TestWufooIntegration:
    """Integration tests for Wufoo Agent"""

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