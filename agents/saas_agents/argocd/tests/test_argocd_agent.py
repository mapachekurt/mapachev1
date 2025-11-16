"""
Tests for ArgoCD Agent
"""

import pytest
from agents.saas_agents.argocd.agent import ArgocdAgent, argocd_agent


class TestArgocdAgent:
    """Test suite for ArgoCD Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ArgocdAgent()
        assert agent.agent_id == "agent_635"
        assert agent.role == "ArgoCD Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "ci_cd"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ArgocdAgent()
        result = agent.execute("test task")
        assert "ArgoCD Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ArgocdAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ArgocdAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_635"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "ci_cd"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert argocd_agent.agent_id == "agent_635"


class TestArgocdIntegration:
    """Integration tests for ArgoCD Agent"""

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