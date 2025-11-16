"""
Tests for Restaurant365 Agent
"""

import pytest
from agents.saas_agents.restaurant365.agent import Restaurant365Agent, restaurant365_agent


class TestRestaurant365Agent:
    """Test suite for Restaurant365 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = Restaurant365Agent()
        assert agent.agent_id == "agent_1165"
        assert agent.role == "Restaurant365 Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "restaurant"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = Restaurant365Agent()
        result = agent.execute("test task")
        assert "Restaurant365 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = Restaurant365Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = Restaurant365Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1165"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "restaurant"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert restaurant365_agent.agent_id == "agent_1165"


class TestRestaurant365Integration:
    """Integration tests for Restaurant365 Agent"""

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