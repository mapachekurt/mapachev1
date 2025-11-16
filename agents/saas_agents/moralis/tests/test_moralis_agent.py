"""
Tests for Moralis Agent
"""

import pytest
from agents.saas_agents.moralis.agent import MoralisAgent, moralis_agent


class TestMoralisAgent:
    """Test suite for Moralis Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MoralisAgent()
        assert agent.agent_id == "agent_1464"
        assert agent.role == "Moralis Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "web3"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MoralisAgent()
        result = agent.execute("test task")
        assert "Moralis Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MoralisAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MoralisAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1464"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "web3"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert moralis_agent.agent_id == "agent_1464"


class TestMoralisIntegration:
    """Integration tests for Moralis Agent"""

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