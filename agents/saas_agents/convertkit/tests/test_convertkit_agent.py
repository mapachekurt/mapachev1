"""
Tests for ConvertKit Agent
"""

import pytest
from agents.saas_agents.convertkit.agent import ConvertkitAgent, convertkit_agent


class TestConvertkitAgent:
    """Test suite for ConvertKit Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ConvertkitAgent()
        assert agent.agent_id == "agent_541"
        assert agent.role == "ConvertKit Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "email_marketing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ConvertkitAgent()
        result = agent.execute("test task")
        assert "ConvertKit Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ConvertkitAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ConvertkitAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_541"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "email_marketing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert convertkit_agent.agent_id == "agent_541"


class TestConvertkitIntegration:
    """Integration tests for ConvertKit Agent"""

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