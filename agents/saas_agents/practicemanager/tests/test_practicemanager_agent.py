"""
Tests for PracticePanther Agent
"""

import pytest
from agents.saas_agents.practicemanager.agent import PracticemanagerAgent, practicemanager_agent


class TestPracticemanagerAgent:
    """Test suite for PracticePanther Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PracticemanagerAgent()
        assert agent.agent_id == "agent_1034"
        assert agent.role == "PracticePanther Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PracticemanagerAgent()
        result = agent.execute("test task")
        assert "PracticePanther Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PracticemanagerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PracticemanagerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1034"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert practicemanager_agent.agent_id == "agent_1034"


class TestPracticemanagerIntegration:
    """Integration tests for PracticePanther Agent"""

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