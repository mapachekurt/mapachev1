"""
Tests for Ansible Agent
"""

import pytest
from agents.saas_agents.ansible.agent import AnsibleAgent, ansible_agent


class TestAnsibleAgent:
    """Test suite for Ansible Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AnsibleAgent()
        assert agent.agent_id == "agent_688"
        assert agent.role == "Ansible Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AnsibleAgent()
        result = agent.execute("test task")
        assert "Ansible Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AnsibleAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AnsibleAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_688"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert ansible_agent.agent_id == "agent_688"


class TestAnsibleIntegration:
    """Integration tests for Ansible Agent"""

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