"""
Tests for Clearbit Agent
"""

import pytest
from agents.saas_agents.clearbit.agent import ClearbitAgent, clearbit_agent


class TestClearbitAgent:
    """Test suite for Clearbit Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ClearbitAgent()
        assert agent.agent_id == "agent_613"
        assert agent.role == "Clearbit Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "lead_generation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ClearbitAgent()
        result = agent.execute("test task")
        assert "Clearbit Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ClearbitAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ClearbitAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_613"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "lead_generation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert clearbit_agent.agent_id == "agent_613"


class TestClearbitIntegration:
    """Integration tests for Clearbit Agent"""

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