"""
Tests for Karate DSL Agent
"""

import pytest
from agents.saas_agents.karate.agent import KarateAgent, karate_agent


class TestKarateAgent:
    """Test suite for Karate DSL Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KarateAgent()
        assert agent.agent_id == "agent_1395"
        assert agent.role == "Karate DSL Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KarateAgent()
        result = agent.execute("test task")
        assert "Karate DSL Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KarateAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KarateAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1395"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert karate_agent.agent_id == "agent_1395"


class TestKarateIntegration:
    """Integration tests for Karate DSL Agent"""

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