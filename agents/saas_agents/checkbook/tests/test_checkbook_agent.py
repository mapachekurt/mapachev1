"""
Tests for Checkbook.io Agent
"""

import pytest
from agents.saas_agents.checkbook.agent import CheckbookAgent, checkbook_agent


class TestCheckbookAgent:
    """Test suite for Checkbook.io Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CheckbookAgent()
        assert agent.agent_id == "agent_1509"
        assert agent.role == "Checkbook.io Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CheckbookAgent()
        result = agent.execute("test task")
        assert "Checkbook.io Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CheckbookAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CheckbookAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1509"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert checkbook_agent.agent_id == "agent_1509"


class TestCheckbookIntegration:
    """Integration tests for Checkbook.io Agent"""

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