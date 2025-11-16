"""
Tests for ClassLink Agent
"""

import pytest
from agents.saas_agents.classlink.agent import ClasslinkAgent, classlink_agent


class TestClasslinkAgent:
    """Test suite for ClassLink Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ClasslinkAgent()
        assert agent.agent_id == "agent_1059"
        assert agent.role == "ClassLink Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "education"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ClasslinkAgent()
        result = agent.execute("test task")
        assert "ClassLink Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ClasslinkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ClasslinkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1059"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "education"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert classlink_agent.agent_id == "agent_1059"


class TestClasslinkIntegration:
    """Integration tests for ClassLink Agent"""

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