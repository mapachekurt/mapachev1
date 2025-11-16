"""
Tests for Formidable Forms Agent
"""

import pytest
from agents.saas_agents.formidable.agent import FormidableAgent, formidable_agent


class TestFormidableAgent:
    """Test suite for Formidable Forms Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FormidableAgent()
        assert agent.agent_id == "agent_886"
        assert agent.role == "Formidable Forms Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "forms"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FormidableAgent()
        result = agent.execute("test task")
        assert "Formidable Forms Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FormidableAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FormidableAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_886"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "forms"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert formidable_agent.agent_id == "agent_886"


class TestFormidableIntegration:
    """Integration tests for Formidable Forms Agent"""

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