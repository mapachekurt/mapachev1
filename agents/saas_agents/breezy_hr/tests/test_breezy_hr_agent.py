"""
Tests for Breezy HR Agent
"""

import pytest
from agents.saas_agents.breezy_hr.agent import BreezyHrAgent, breezy_hr_agent


class TestBreezyHrAgent:
    """Test suite for Breezy HR Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BreezyHrAgent()
        assert agent.agent_id == "agent_944"
        assert agent.role == "Breezy HR Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BreezyHrAgent()
        result = agent.execute("test task")
        assert "Breezy HR Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BreezyHrAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BreezyHrAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_944"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert breezy_hr_agent.agent_id == "agent_944"


class TestBreezyHrIntegration:
    """Integration tests for Breezy HR Agent"""

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