"""
Tests for Clear Books Agent
"""

import pytest
from agents.saas_agents.clearbooks.agent import ClearbooksAgent, clearbooks_agent


class TestClearbooksAgent:
    """Test suite for Clear Books Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ClearbooksAgent()
        assert agent.agent_id == "agent_899"
        assert agent.role == "Clear Books Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "finance"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ClearbooksAgent()
        result = agent.execute("test task")
        assert "Clear Books Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ClearbooksAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ClearbooksAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_899"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "finance"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert clearbooks_agent.agent_id == "agent_899"


class TestClearbooksIntegration:
    """Integration tests for Clear Books Agent"""

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