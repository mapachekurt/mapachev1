"""
Tests for Tidio Agent
"""

import pytest
from agents.saas_agents.tidio.agent import TidioAgent, tidio_agent


class TestTidioAgent:
    """Test suite for Tidio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TidioAgent()
        assert agent.agent_id == "agent_995"
        assert agent.role == "Tidio Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TidioAgent()
        result = agent.execute("test task")
        assert "Tidio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TidioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TidioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_995"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert tidio_agent.agent_id == "agent_995"


class TestTidioIntegration:
    """Integration tests for Tidio Agent"""

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