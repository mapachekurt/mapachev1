"""
Tests for NextGen Healthcare Agent
"""

import pytest
from agents.saas_agents.nextgen.agent import NextgenAgent, nextgen_agent


class TestNextgenAgent:
    """Test suite for NextGen Healthcare Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = NextgenAgent()
        assert agent.agent_id == "agent_1016"
        assert agent.role == "NextGen Healthcare Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "healthcare"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = NextgenAgent()
        result = agent.execute("test task")
        assert "NextGen Healthcare Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = NextgenAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = NextgenAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1016"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "healthcare"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert nextgen_agent.agent_id == "agent_1016"


class TestNextgenIntegration:
    """Integration tests for NextGen Healthcare Agent"""

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