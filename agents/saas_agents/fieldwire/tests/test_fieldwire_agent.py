"""
Tests for Fieldwire Agent
"""

import pytest
from agents.saas_agents.fieldwire.agent import FieldwireAgent, fieldwire_agent


class TestFieldwireAgent:
    """Test suite for Fieldwire Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = FieldwireAgent()
        assert agent.agent_id == "agent_1095"
        assert agent.role == "Fieldwire Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "construction"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = FieldwireAgent()
        result = agent.execute("test task")
        assert "Fieldwire Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = FieldwireAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = FieldwireAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1095"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "construction"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert fieldwire_agent.agent_id == "agent_1095"


class TestFieldwireIntegration:
    """Integration tests for Fieldwire Agent"""

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