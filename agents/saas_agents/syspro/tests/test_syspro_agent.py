"""
Tests for SYSPRO Agent
"""

import pytest
from agents.saas_agents.syspro.agent import SysproAgent, syspro_agent


class TestSysproAgent:
    """Test suite for SYSPRO Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SysproAgent()
        assert agent.agent_id == "agent_1297"
        assert agent.role == "SYSPRO Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "manufacturing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SysproAgent()
        result = agent.execute("test task")
        assert "SYSPRO Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SysproAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SysproAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1297"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "manufacturing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert syspro_agent.agent_id == "agent_1297"


class TestSysproIntegration:
    """Integration tests for SYSPRO Agent"""

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