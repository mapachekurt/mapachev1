"""
Tests for Chainlink Agent
"""

import pytest
from agents.saas_agents.chainlink.agent import ChainlinkAgent, chainlink_agent


class TestChainlinkAgent:
    """Test suite for Chainlink Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ChainlinkAgent()
        assert agent.agent_id == "agent_1466"
        assert agent.role == "Chainlink Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "web3"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ChainlinkAgent()
        result = agent.execute("test task")
        assert "Chainlink Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ChainlinkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ChainlinkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1466"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "web3"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert chainlink_agent.agent_id == "agent_1466"


class TestChainlinkIntegration:
    """Integration tests for Chainlink Agent"""

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