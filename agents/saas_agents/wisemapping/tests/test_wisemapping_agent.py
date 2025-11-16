"""
Tests for WiseMapping Agent
"""

import pytest
from agents.saas_agents.wisemapping.agent import WisemappingAgent, wisemapping_agent


class TestWisemappingAgent:
    """Test suite for WiseMapping Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WisemappingAgent()
        assert agent.agent_id == "agent_1350"
        assert agent.role == "WiseMapping Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "collaboration"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WisemappingAgent()
        result = agent.execute("test task")
        assert "WiseMapping Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WisemappingAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WisemappingAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1350"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "collaboration"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wisemapping_agent.agent_id == "agent_1350"


class TestWisemappingIntegration:
    """Integration tests for WiseMapping Agent"""

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