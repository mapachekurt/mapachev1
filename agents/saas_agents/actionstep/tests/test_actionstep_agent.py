"""
Tests for Actionstep Agent
"""

import pytest
from agents.saas_agents.actionstep.agent import ActionstepAgent, actionstep_agent


class TestActionstepAgent:
    """Test suite for Actionstep Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ActionstepAgent()
        assert agent.agent_id == "agent_1040"
        assert agent.role == "Actionstep Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "legal"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ActionstepAgent()
        result = agent.execute("test task")
        assert "Actionstep Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ActionstepAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ActionstepAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1040"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "legal"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert actionstep_agent.agent_id == "agent_1040"


class TestActionstepIntegration:
    """Integration tests for Actionstep Agent"""

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