"""
Tests for Helm Agent
"""

import pytest
from agents.saas_agents.helm.agent import HelmAgent, helm_agent


class TestHelmAgent:
    """Test suite for Helm Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HelmAgent()
        assert agent.agent_id == "agent_694"
        assert agent.role == "Helm Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HelmAgent()
        result = agent.execute("test task")
        assert "Helm Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HelmAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HelmAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_694"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert helm_agent.agent_id == "agent_694"


class TestHelmIntegration:
    """Integration tests for Helm Agent"""

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