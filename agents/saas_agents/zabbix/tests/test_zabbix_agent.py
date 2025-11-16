"""
Tests for Zabbix Agent
"""

import pytest
from agents.saas_agents.zabbix.agent import ZabbixAgent, zabbix_agent


class TestZabbixAgent:
    """Test suite for Zabbix Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ZabbixAgent()
        assert agent.agent_id == "agent_679"
        assert agent.role == "Zabbix Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "monitoring"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ZabbixAgent()
        result = agent.execute("test task")
        assert "Zabbix Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ZabbixAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ZabbixAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_679"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "monitoring"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert zabbix_agent.agent_id == "agent_679"


class TestZabbixIntegration:
    """Integration tests for Zabbix Agent"""

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