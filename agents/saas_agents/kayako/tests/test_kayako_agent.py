"""
Tests for Kayako Agent
"""

import pytest
from agents.saas_agents.kayako.agent import KayakoAgent, kayako_agent


class TestKayakoAgent:
    """Test suite for Kayako Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KayakoAgent()
        assert agent.agent_id == "agent_989"
        assert agent.role == "Kayako Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KayakoAgent()
        result = agent.execute("test task")
        assert "Kayako Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KayakoAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KayakoAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_989"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kayako_agent.agent_id == "agent_989"


class TestKayakoIntegration:
    """Integration tests for Kayako Agent"""

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