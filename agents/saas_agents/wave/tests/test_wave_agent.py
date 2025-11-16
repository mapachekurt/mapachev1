"""
Tests for Wave Accounting Agent
"""

import pytest
from agents.saas_agents.wave.agent import WaveAgent, wave_agent


class TestWaveAgent:
    """Test suite for Wave Accounting Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WaveAgent()
        assert agent.agent_id == "agent_894"
        assert agent.role == "Wave Accounting Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WaveAgent()
        result = agent.execute("test task")
        assert "Wave Accounting Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WaveAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WaveAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_894"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert wave_agent.agent_id == "agent_894"


class TestWaveIntegration:
    """Integration tests for Wave Accounting Agent"""

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