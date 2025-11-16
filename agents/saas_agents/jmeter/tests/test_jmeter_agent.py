"""
Tests for Apache JMeter Agent
"""

import pytest
from agents.saas_agents.jmeter.agent import JmeterAgent, jmeter_agent


class TestJmeterAgent:
    """Test suite for Apache JMeter Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JmeterAgent()
        assert agent.agent_id == "agent_1404"
        assert agent.role == "Apache JMeter Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "testing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JmeterAgent()
        result = agent.execute("test task")
        assert "Apache JMeter Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JmeterAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JmeterAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1404"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "testing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert jmeter_agent.agent_id == "agent_1404"


class TestJmeterIntegration:
    """Integration tests for Apache JMeter Agent"""

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