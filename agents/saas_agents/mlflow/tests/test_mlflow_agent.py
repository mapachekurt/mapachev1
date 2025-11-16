"""
Tests for MLflow Agent
"""

import pytest
from agents.saas_agents.mlflow.agent import MlflowAgent, mlflow_agent


class TestMlflowAgent:
    """Test suite for MLflow Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = MlflowAgent()
        assert agent.agent_id == "agent_1416"
        assert agent.role == "MLflow Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = MlflowAgent()
        result = agent.execute("test task")
        assert "MLflow Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = MlflowAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = MlflowAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1416"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert mlflow_agent.agent_id == "agent_1416"


class TestMlflowIntegration:
    """Integration tests for MLflow Agent"""

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