"""
Tests for Buildertrend Agent
"""

import pytest
from agents.saas_agents.buildertrend.agent import BuildertrendAgent, buildertrend_agent


class TestBuildertrendAgent:
    """Test suite for Buildertrend Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BuildertrendAgent()
        assert agent.agent_id == "agent_1093"
        assert agent.role == "Buildertrend Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BuildertrendAgent()
        result = agent.execute("test task")
        assert "Buildertrend Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BuildertrendAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BuildertrendAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1093"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert buildertrend_agent.agent_id == "agent_1093"


class TestBuildertrendIntegration:
    """Integration tests for Buildertrend Agent"""

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