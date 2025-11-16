"""
Tests for Mural Agent
"""

import pytest
from agents.saas_agents.mural.agent import MuralAgent, mural_agent


class TestMuralAgent:
    """Test suite for Mural Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MuralAgent()
        assert agent.agent_id == "agent_1339"
        assert agent.role == "Mural Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "collaboration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MuralAgent()
        result = agent.execute("test task")
        assert "Mural Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MuralAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MuralAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1339"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "collaboration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mural_agent.agent_id == "agent_1339"


class TestMuralIntegration:
    """Integration tests for Mural Agent"""

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