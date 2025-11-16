"""
Tests for Cropio Agent
"""

import pytest
from agents.saas_agents.cropio.agent import CropioAgent, cropio_agent


class TestCropioAgent:
    """Test suite for Cropio Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CropioAgent()
        assert agent.agent_id == "agent_1277"
        assert agent.role == "Cropio Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "agriculture"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CropioAgent()
        result = agent.execute("test task")
        assert "Cropio Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CropioAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CropioAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1277"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "agriculture"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert cropio_agent.agent_id == "agent_1277"


class TestCropioIntegration:
    """Integration tests for Cropio Agent"""

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