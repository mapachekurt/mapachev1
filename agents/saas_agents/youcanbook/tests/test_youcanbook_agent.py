"""
Tests for YouCanBook.me Agent
"""

import pytest
from agents.saas_agents.youcanbook.agent import YoucanbookAgent, youcanbook_agent


class TestYoucanbookAgent:
    """Test suite for YouCanBook.me Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = YoucanbookAgent()
        assert agent.agent_id == "agent_850"
        assert agent.role == "YouCanBook.me Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "scheduling"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = YoucanbookAgent()
        result = agent.execute("test task")
        assert "YouCanBook.me Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = YoucanbookAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = YoucanbookAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_850"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "scheduling"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert youcanbook_agent.agent_id == "agent_850"


class TestYoucanbookIntegration:
    """Integration tests for YouCanBook.me Agent"""

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