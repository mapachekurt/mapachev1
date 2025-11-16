"""
Tests for Pipedrive Agent
"""

import pytest
from agents.saas_agents.pipedrive.agent import PipedriveAgent, pipedrive_agent


class TestPipedriveAgent:
    """Test suite for Pipedrive Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = PipedriveAgent()
        assert agent.agent_id == "agent_572"
        assert agent.role == "Pipedrive Specialist"
        assert agent.tier == "Marketing & Sales"
        assert agent.category == "crm"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = PipedriveAgent()
        result = agent.execute("test task")
        assert "Pipedrive Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = PipedriveAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = PipedriveAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_572"
        assert config["tier"] == "Marketing & Sales"
        assert config["category"] == "crm"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert pipedrive_agent.agent_id == "agent_572"


class TestPipedriveIntegration:
    """Integration tests for Pipedrive Agent"""

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