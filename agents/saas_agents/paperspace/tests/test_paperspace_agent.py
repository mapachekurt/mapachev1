"""
Tests for Paperspace Agent
"""

import pytest
from agents.saas_agents.paperspace.agent import PaperspaceAgent, paperspace_agent


class TestPaperspaceAgent:
    """Test suite for Paperspace Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PaperspaceAgent()
        assert agent.agent_id == "agent_1422"
        assert agent.role == "Paperspace Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PaperspaceAgent()
        result = agent.execute("test task")
        assert "Paperspace Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PaperspaceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PaperspaceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1422"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert paperspace_agent.agent_id == "agent_1422"


class TestPaperspaceIntegration:
    """Integration tests for Paperspace Agent"""

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