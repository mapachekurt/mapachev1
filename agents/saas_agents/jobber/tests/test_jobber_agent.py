"""
Tests for Jobber Agent
"""

import pytest
from agents.saas_agents.jobber.agent import JobberAgent, jobber_agent


class TestJobberAgent:
    """Test suite for Jobber Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = JobberAgent()
        assert agent.agent_id == "agent_1102"
        assert agent.role == "Jobber Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = JobberAgent()
        result = agent.execute("test task")
        assert "Jobber Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = JobberAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = JobberAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1102"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert jobber_agent.agent_id == "agent_1102"


class TestJobberIntegration:
    """Integration tests for Jobber Agent"""

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