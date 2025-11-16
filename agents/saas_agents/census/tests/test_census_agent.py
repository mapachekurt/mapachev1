"""
Tests for Census Agent
"""

import pytest
from agents.saas_agents.census.agent import CensusAgent, census_agent


class TestCensusAgent:
    """Test suite for Census Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CensusAgent()
        assert agent.agent_id == "agent_1386"
        assert agent.role == "Census Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "data"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CensusAgent()
        result = agent.execute("test task")
        assert "Census Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CensusAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CensusAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1386"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "data"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert census_agent.agent_id == "agent_1386"


class TestCensusIntegration:
    """Integration tests for Census Agent"""

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