"""
Tests for Bitbucket Agent
"""

import pytest
from agents.saas_agents.bitbucket.agent import BitbucketAgent, bitbucket_agent


class TestBitbucketAgent:
    """Test suite for Bitbucket Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BitbucketAgent()
        assert agent.agent_id == "agent_528"
        assert agent.role == "Bitbucket Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "development"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BitbucketAgent()
        result = agent.execute("test task")
        assert "Bitbucket Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BitbucketAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BitbucketAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_528"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "development"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert bitbucket_agent.agent_id == "agent_528"


class TestBitbucketIntegration:
    """Integration tests for Bitbucket Agent"""

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