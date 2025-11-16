"""
Tests for k6 Agent
"""

import pytest
from agents.saas_agents.k6.agent import K6Agent, k6_agent


class TestK6Agent:
    """Test suite for k6 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = K6Agent()
        assert agent.agent_id == "agent_1405"
        assert agent.role == "k6 Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = K6Agent()
        result = agent.execute("test task")
        assert "k6 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = K6Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = K6Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1405"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert k6_agent.agent_id == "agent_1405"


class TestK6Integration:
    """Integration tests for k6 Agent"""

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