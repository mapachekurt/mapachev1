"""
Tests for Make (Integromat) Agent
"""

import pytest
from agents.saas_agents.make.agent import MakeAgent, make_agent


class TestMakeAgent:
    """Test suite for Make (Integromat) Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MakeAgent()
        assert agent.agent_id == "agent_1329"
        assert agent.role == "Make (Integromat) Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MakeAgent()
        result = agent.execute("test task")
        assert "Make (Integromat) Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MakeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MakeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1329"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert make_agent.agent_id == "agent_1329"


class TestMakeIntegration:
    """Integration tests for Make (Integromat) Agent"""

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