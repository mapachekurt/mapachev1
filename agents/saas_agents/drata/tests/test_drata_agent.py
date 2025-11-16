"""
Tests for Drata Agent
"""

import pytest
from agents.saas_agents.drata.agent import DrataAgent, drata_agent


class TestDrataAgent:
    """Test suite for Drata Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DrataAgent()
        assert agent.agent_id == "agent_1446"
        assert agent.role == "Drata Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "compliance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DrataAgent()
        result = agent.execute("test task")
        assert "Drata Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DrataAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DrataAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1446"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "compliance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert drata_agent.agent_id == "agent_1446"


class TestDrataIntegration:
    """Integration tests for Drata Agent"""

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