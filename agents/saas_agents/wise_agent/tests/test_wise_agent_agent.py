"""
Tests for Wise Agent Agent
"""

import pytest
from agents.saas_agents.wise_agent.agent import WiseAgentAgent, wise_agent_agent


class TestWiseAgentAgent:
    """Test suite for Wise Agent Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WiseAgentAgent()
        assert agent.agent_id == "agent_1082"
        assert agent.role == "Wise Agent Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "real_estate"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WiseAgentAgent()
        result = agent.execute("test task")
        assert "Wise Agent Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WiseAgentAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WiseAgentAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1082"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "real_estate"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wise_agent_agent.agent_id == "agent_1082"


class TestWiseAgentIntegration:
    """Integration tests for Wise Agent Agent"""

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