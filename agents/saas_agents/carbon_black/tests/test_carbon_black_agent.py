"""
Tests for Carbon Black Agent
"""

import pytest
from agents.saas_agents.carbon_black.agent import CarbonBlackAgent, carbon_black_agent


class TestCarbonBlackAgent:
    """Test suite for Carbon Black Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CarbonBlackAgent()
        assert agent.agent_id == "agent_1440"
        assert agent.role == "Carbon Black Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CarbonBlackAgent()
        result = agent.execute("test task")
        assert "Carbon Black Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CarbonBlackAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CarbonBlackAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1440"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert carbon_black_agent.agent_id == "agent_1440"


class TestCarbonBlackIntegration:
    """Integration tests for Carbon Black Agent"""

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