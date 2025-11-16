"""
Tests for Tresorit Agent
"""

import pytest
from agents.saas_agents.tresorit.agent import TresoritAgent, tresorit_agent


class TestTresoritAgent:
    """Test suite for Tresorit Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TresoritAgent()
        assert agent.agent_id == "agent_789"
        assert agent.role == "Tresorit Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "file_sharing"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TresoritAgent()
        result = agent.execute("test task")
        assert "Tresorit Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TresoritAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TresoritAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_789"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "file_sharing"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert tresorit_agent.agent_id == "agent_789"


class TestTresoritIntegration:
    """Integration tests for Tresorit Agent"""

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