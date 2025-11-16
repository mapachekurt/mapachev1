"""
Tests for PC America Agent
"""

import pytest
from agents.saas_agents.pcamerica.agent import PcamericaAgent, pcamerica_agent


class TestPcamericaAgent:
    """Test suite for PC America Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PcamericaAgent()
        assert agent.agent_id == "agent_1187"
        assert agent.role == "PC America Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PcamericaAgent()
        result = agent.execute("test task")
        assert "PC America Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PcamericaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PcamericaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1187"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pcamerica_agent.agent_id == "agent_1187"


class TestPcamericaIntegration:
    """Integration tests for PC America Agent"""

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