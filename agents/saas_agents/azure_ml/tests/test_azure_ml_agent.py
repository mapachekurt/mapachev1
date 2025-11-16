"""
Tests for Azure Machine Learning Agent
"""

import pytest
from agents.saas_agents.azure_ml.agent import AzureMlAgent, azure_ml_agent


class TestAzureMlAgent:
    """Test suite for Azure Machine Learning Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AzureMlAgent()
        assert agent.agent_id == "agent_1426"
        assert agent.role == "Azure Machine Learning Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AzureMlAgent()
        result = agent.execute("test task")
        assert "Azure Machine Learning Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AzureMlAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AzureMlAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1426"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert azure_ml_agent.agent_id == "agent_1426"


class TestAzureMlIntegration:
    """Integration tests for Azure Machine Learning Agent"""

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