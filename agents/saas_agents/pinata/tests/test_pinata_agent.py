"""
Tests for Pinata Agent
"""

import pytest
from agents.saas_agents.pinata.agent import PinataAgent, pinata_agent


class TestPinataAgent:
    """Test suite for Pinata Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PinataAgent()
        assert agent.agent_id == "agent_1467"
        assert agent.role == "Pinata Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "web3"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PinataAgent()
        result = agent.execute("test task")
        assert "Pinata Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PinataAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PinataAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1467"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "web3"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pinata_agent.agent_id == "agent_1467"


class TestPinataIntegration:
    """Integration tests for Pinata Agent"""

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