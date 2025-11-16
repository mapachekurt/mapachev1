"""
Tests for Sisense Advanced Agent
"""

import pytest
from agents.saas_agents.sisense_advanced.agent import SisenseAdvancedAgent, sisense_advanced_agent


class TestSisenseAdvancedAgent:
    """Test suite for Sisense Advanced Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SisenseAdvancedAgent()
        assert agent.agent_id == "agent_1364"
        assert agent.role == "Sisense Advanced Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "bi"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SisenseAdvancedAgent()
        result = agent.execute("test task")
        assert "Sisense Advanced Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SisenseAdvancedAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SisenseAdvancedAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1364"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "bi"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert sisense_advanced_agent.agent_id == "agent_1364"


class TestSisenseAdvancedIntegration:
    """Integration tests for Sisense Advanced Agent"""

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