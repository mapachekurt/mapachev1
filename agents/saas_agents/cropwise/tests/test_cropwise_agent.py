"""
Tests for Cropwise Agent
"""

import pytest
from agents.saas_agents.cropwise.agent import CropwiseAgent, cropwise_agent


class TestCropwiseAgent:
    """Test suite for Cropwise Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CropwiseAgent()
        assert agent.agent_id == "agent_1285"
        assert agent.role == "Cropwise Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "agriculture"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CropwiseAgent()
        result = agent.execute("test task")
        assert "Cropwise Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CropwiseAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CropwiseAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1285"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "agriculture"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cropwise_agent.agent_id == "agent_1285"


class TestCropwiseIntegration:
    """Integration tests for Cropwise Agent"""

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