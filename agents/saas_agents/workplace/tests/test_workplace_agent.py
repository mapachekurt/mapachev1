"""
Tests for Meta Workplace Agent
"""

import pytest
from agents.saas_agents.workplace.agent import WorkplaceAgent, workplace_agent


class TestWorkplaceAgent:
    """Test suite for Meta Workplace Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WorkplaceAgent()
        assert agent.agent_id == "agent_846"
        assert agent.role == "Meta Workplace Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WorkplaceAgent()
        result = agent.execute("test task")
        assert "Meta Workplace Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WorkplaceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WorkplaceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_846"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert workplace_agent.agent_id == "agent_846"


class TestWorkplaceIntegration:
    """Integration tests for Meta Workplace Agent"""

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