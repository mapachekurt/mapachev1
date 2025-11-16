"""
Tests for Yellowfin BI Agent
"""

import pytest
from agents.saas_agents.yellowfin.agent import YellowfinAgent, yellowfin_agent


class TestYellowfinAgent:
    """Test suite for Yellowfin BI Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = YellowfinAgent()
        assert agent.agent_id == "agent_1367"
        assert agent.role == "Yellowfin BI Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = YellowfinAgent()
        result = agent.execute("test task")
        assert "Yellowfin BI Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = YellowfinAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = YellowfinAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1367"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert yellowfin_agent.agent_id == "agent_1367"


class TestYellowfinIntegration:
    """Integration tests for Yellowfin BI Agent"""

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