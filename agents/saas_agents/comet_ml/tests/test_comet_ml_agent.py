"""
Tests for Comet ML Agent
"""

import pytest
from agents.saas_agents.comet_ml.agent import CometMlAgent, comet_ml_agent


class TestCometMlAgent:
    """Test suite for Comet ML Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CometMlAgent()
        assert agent.agent_id == "agent_1419"
        assert agent.role == "Comet ML Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CometMlAgent()
        result = agent.execute("test task")
        assert "Comet ML Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CometMlAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CometMlAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1419"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert comet_ml_agent.agent_id == "agent_1419"


class TestCometMlIntegration:
    """Integration tests for Comet ML Agent"""

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