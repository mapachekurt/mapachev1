"""
Tests for Geneva Agent
"""

import pytest
from agents.saas_agents.geneva.agent import GenevaAgent, geneva_agent


class TestGenevaAgent:
    """Test suite for Geneva Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GenevaAgent()
        assert agent.agent_id == "agent_1251"
        assert agent.role == "Geneva Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "membership"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GenevaAgent()
        result = agent.execute("test task")
        assert "Geneva Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GenevaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GenevaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1251"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "membership"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert geneva_agent.agent_id == "agent_1251"


class TestGenevaIntegration:
    """Integration tests for Geneva Agent"""

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