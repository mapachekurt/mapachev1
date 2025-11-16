"""
Tests for ServiceM8 Agent
"""

import pytest
from agents.saas_agents.servicem8.agent import Servicem8Agent, servicem8_agent


class TestServicem8Agent:
    """Test suite for ServiceM8 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = Servicem8Agent()
        assert agent.agent_id == "agent_1105"
        assert agent.role == "ServiceM8 Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = Servicem8Agent()
        result = agent.execute("test task")
        assert "ServiceM8 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = Servicem8Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = Servicem8Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1105"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert servicem8_agent.agent_id == "agent_1105"


class TestServicem8Integration:
    """Integration tests for ServiceM8 Agent"""

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