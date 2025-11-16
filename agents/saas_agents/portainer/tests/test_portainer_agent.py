"""
Tests for Portainer Agent
"""

import pytest
from agents.saas_agents.portainer.agent import PortainerAgent, portainer_agent


class TestPortainerAgent:
    """Test suite for Portainer Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PortainerAgent()
        assert agent.agent_id == "agent_701"
        assert agent.role == "Portainer Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PortainerAgent()
        result = agent.execute("test task")
        assert "Portainer Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PortainerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PortainerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_701"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert portainer_agent.agent_id == "agent_701"


class TestPortainerIntegration:
    """Integration tests for Portainer Agent"""

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