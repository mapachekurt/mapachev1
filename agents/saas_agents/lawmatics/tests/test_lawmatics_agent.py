"""
Tests for Lawmatics Agent
"""

import pytest
from agents.saas_agents.lawmatics.agent import LawmaticsAgent, lawmatics_agent


class TestLawmaticsAgent:
    """Test suite for Lawmatics Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LawmaticsAgent()
        assert agent.agent_id == "agent_1037"
        assert agent.role == "Lawmatics Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LawmaticsAgent()
        result = agent.execute("test task")
        assert "Lawmatics Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LawmaticsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LawmaticsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1037"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lawmatics_agent.agent_id == "agent_1037"


class TestLawmaticsIntegration:
    """Integration tests for Lawmatics Agent"""

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