"""
Tests for Podio Agent
"""

import pytest
from agents.saas_agents.podio.agent import PodioAgent, podio_agent


class TestPodioAgent:
    """Test suite for Podio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PodioAgent()
        assert agent.agent_id == "agent_807"
        assert agent.role == "Podio Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "project_management"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PodioAgent()
        result = agent.execute("test task")
        assert "Podio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PodioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PodioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_807"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "project_management"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert podio_agent.agent_id == "agent_807"


class TestPodioIntegration:
    """Integration tests for Podio Agent"""

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