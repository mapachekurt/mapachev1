"""
Tests for Vagrant Agent
"""

import pytest
from agents.saas_agents.vagrant.agent import VagrantAgent, vagrant_agent


class TestVagrantAgent:
    """Test suite for Vagrant Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VagrantAgent()
        assert agent.agent_id == "agent_695"
        assert agent.role == "Vagrant Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VagrantAgent()
        result = agent.execute("test task")
        assert "Vagrant Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VagrantAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VagrantAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_695"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert vagrant_agent.agent_id == "agent_695"


class TestVagrantIntegration:
    """Integration tests for Vagrant Agent"""

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