"""
Tests for Keela Agent
"""

import pytest
from agents.saas_agents.keela.agent import KeelaAgent, keela_agent


class TestKeelaAgent:
    """Test suite for Keela Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KeelaAgent()
        assert agent.agent_id == "agent_1264"
        assert agent.role == "Keela Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "nonprofit"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KeelaAgent()
        result = agent.execute("test task")
        assert "Keela Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KeelaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KeelaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1264"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "nonprofit"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert keela_agent.agent_id == "agent_1264"


class TestKeelaIntegration:
    """Integration tests for Keela Agent"""

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