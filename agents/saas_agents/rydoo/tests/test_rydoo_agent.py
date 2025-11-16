"""
Tests for Rydoo Agent
"""

import pytest
from agents.saas_agents.rydoo.agent import RydooAgent, rydoo_agent


class TestRydooAgent:
    """Test suite for Rydoo Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RydooAgent()
        assert agent.agent_id == "agent_912"
        assert agent.role == "Rydoo Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RydooAgent()
        result = agent.execute("test task")
        assert "Rydoo Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RydooAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RydooAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_912"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rydoo_agent.agent_id == "agent_912"


class TestRydooIntegration:
    """Integration tests for Rydoo Agent"""

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