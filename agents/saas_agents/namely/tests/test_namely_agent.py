"""
Tests for Namely Agent
"""

import pytest
from agents.saas_agents.namely.agent import NamelyAgent, namely_agent


class TestNamelyAgent:
    """Test suite for Namely Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NamelyAgent()
        assert agent.agent_id == "agent_956"
        assert agent.role == "Namely Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NamelyAgent()
        result = agent.execute("test task")
        assert "Namely Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NamelyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NamelyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_956"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert namely_agent.agent_id == "agent_956"


class TestNamelyIntegration:
    """Integration tests for Namely Agent"""

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