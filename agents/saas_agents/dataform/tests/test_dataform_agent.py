"""
Tests for Dataform Agent
"""

import pytest
from agents.saas_agents.dataform.agent import DataformAgent, dataform_agent


class TestDataformAgent:
    """Test suite for Dataform Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DataformAgent()
        assert agent.agent_id == "agent_1385"
        assert agent.role == "Dataform Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "data"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DataformAgent()
        result = agent.execute("test task")
        assert "Dataform Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DataformAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DataformAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1385"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "data"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dataform_agent.agent_id == "agent_1385"


class TestDataformIntegration:
    """Integration tests for Dataform Agent"""

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