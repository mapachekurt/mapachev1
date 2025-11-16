"""
Tests for Cortex Agent
"""

import pytest
from agents.saas_agents.cortex.agent import CortexAgent, cortex_agent


class TestCortexAgent:
    """Test suite for Cortex Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CortexAgent()
        assert agent.agent_id == "agent_1430"
        assert agent.role == "Cortex Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CortexAgent()
        result = agent.execute("test task")
        assert "Cortex Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CortexAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CortexAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1430"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cortex_agent.agent_id == "agent_1430"


class TestCortexIntegration:
    """Integration tests for Cortex Agent"""

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