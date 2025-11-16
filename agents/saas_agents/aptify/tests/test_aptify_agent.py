"""
Tests for Aptify Agent
"""

import pytest
from agents.saas_agents.aptify.agent import AptifyAgent, aptify_agent


class TestAptifyAgent:
    """Test suite for Aptify Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AptifyAgent()
        assert agent.agent_id == "agent_1244"
        assert agent.role == "Aptify Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "membership"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AptifyAgent()
        result = agent.execute("test task")
        assert "Aptify Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AptifyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AptifyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1244"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "membership"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aptify_agent.agent_id == "agent_1244"


class TestAptifyIntegration:
    """Integration tests for Aptify Agent"""

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