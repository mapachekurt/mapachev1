"""
Tests for Groove Agent
"""

import pytest
from agents.saas_agents.groovehq.agent import GroovehqAgent, groovehq_agent


class TestGroovehqAgent:
    """Test suite for Groove Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GroovehqAgent()
        assert agent.agent_id == "agent_990"
        assert agent.role == "Groove Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GroovehqAgent()
        result = agent.execute("test task")
        assert "Groove Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GroovehqAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GroovehqAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_990"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert groovehq_agent.agent_id == "agent_990"


class TestGroovehqIntegration:
    """Integration tests for Groove Agent"""

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