"""
Tests for Chartio Agent
"""

import pytest
from agents.saas_agents.chartio.agent import ChartioAgent, chartio_agent


class TestChartioAgent:
    """Test suite for Chartio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ChartioAgent()
        assert agent.agent_id == "agent_1356"
        assert agent.role == "Chartio Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ChartioAgent()
        result = agent.execute("test task")
        assert "Chartio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ChartioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ChartioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1356"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert chartio_agent.agent_id == "agent_1356"


class TestChartioIntegration:
    """Integration tests for Chartio Agent"""

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