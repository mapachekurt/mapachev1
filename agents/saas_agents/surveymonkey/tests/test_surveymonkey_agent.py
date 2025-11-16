"""
Tests for SurveyMonkey Agent
"""

import pytest
from agents.saas_agents.surveymonkey.agent import SurveymonkeyAgent, surveymonkey_agent


class TestSurveymonkeyAgent:
    """Test suite for SurveyMonkey Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SurveymonkeyAgent()
        assert agent.agent_id == "agent_879"
        assert agent.role == "SurveyMonkey Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SurveymonkeyAgent()
        result = agent.execute("test task")
        assert "SurveyMonkey Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SurveymonkeyAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SurveymonkeyAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_879"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert surveymonkey_agent.agent_id == "agent_879"


class TestSurveymonkeyIntegration:
    """Integration tests for SurveyMonkey Agent"""

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