"""
Tests for Locust Agent
"""

import pytest
from agents.saas_agents.locust.agent import LocustAgent, locust_agent


class TestLocustAgent:
    """Test suite for Locust Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LocustAgent()
        assert agent.agent_id == "agent_1407"
        assert agent.role == "Locust Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LocustAgent()
        result = agent.execute("test task")
        assert "Locust Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LocustAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LocustAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1407"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert locust_agent.agent_id == "agent_1407"


class TestLocustIntegration:
    """Integration tests for Locust Agent"""

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