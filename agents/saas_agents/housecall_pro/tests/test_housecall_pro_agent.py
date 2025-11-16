"""
Tests for Housecall Pro Agent
"""

import pytest
from agents.saas_agents.housecall_pro.agent import HousecallProAgent, housecall_pro_agent


class TestHousecallProAgent:
    """Test suite for Housecall Pro Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HousecallProAgent()
        assert agent.agent_id == "agent_1104"
        assert agent.role == "Housecall Pro Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HousecallProAgent()
        result = agent.execute("test task")
        assert "Housecall Pro Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HousecallProAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HousecallProAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1104"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert housecall_pro_agent.agent_id == "agent_1104"


class TestHousecallProIntegration:
    """Integration tests for Housecall Pro Agent"""

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