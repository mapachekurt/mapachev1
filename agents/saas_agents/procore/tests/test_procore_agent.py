"""
Tests for Procore Agent
"""

import pytest
from agents.saas_agents.procore.agent import ProcoreAgent, procore_agent


class TestProcoreAgent:
    """Test suite for Procore Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ProcoreAgent()
        assert agent.agent_id == "agent_1092"
        assert agent.role == "Procore Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ProcoreAgent()
        result = agent.execute("test task")
        assert "Procore Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ProcoreAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ProcoreAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1092"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert procore_agent.agent_id == "agent_1092"


class TestProcoreIntegration:
    """Integration tests for Procore Agent"""

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