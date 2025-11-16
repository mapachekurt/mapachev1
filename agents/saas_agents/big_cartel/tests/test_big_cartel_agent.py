"""
Tests for Big Cartel Agent
"""

import pytest
from agents.saas_agents.big_cartel.agent import BigCartelAgent, big_cartel_agent


class TestBigCartelAgent:
    """Test suite for Big Cartel Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BigCartelAgent()
        assert agent.agent_id == "agent_973"
        assert agent.role == "Big Cartel Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ecommerce"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BigCartelAgent()
        result = agent.execute("test task")
        assert "Big Cartel Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BigCartelAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BigCartelAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_973"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ecommerce"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert big_cartel_agent.agent_id == "agent_973"


class TestBigCartelIntegration:
    """Integration tests for Big Cartel Agent"""

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