"""
Tests for Square for Retail Agent
"""

import pytest
from agents.saas_agents.square_retail.agent import SquareRetailAgent, square_retail_agent


class TestSquareRetailAgent:
    """Test suite for Square for Retail Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SquareRetailAgent()
        assert agent.agent_id == "agent_1173"
        assert agent.role == "Square for Retail Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SquareRetailAgent()
        result = agent.execute("test task")
        assert "Square for Retail Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SquareRetailAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SquareRetailAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1173"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert square_retail_agent.agent_id == "agent_1173"


class TestSquareRetailIntegration:
    """Integration tests for Square for Retail Agent"""

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