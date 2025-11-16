"""
Tests for Lightspeed Retail Agent
"""

import pytest
from agents.saas_agents.lightspeed_retail.agent import LightspeedRetailAgent, lightspeed_retail_agent


class TestLightspeedRetailAgent:
    """Test suite for Lightspeed Retail Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LightspeedRetailAgent()
        assert agent.agent_id == "agent_1175"
        assert agent.role == "Lightspeed Retail Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LightspeedRetailAgent()
        result = agent.execute("test task")
        assert "Lightspeed Retail Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LightspeedRetailAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LightspeedRetailAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1175"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lightspeed_retail_agent.agent_id == "agent_1175"


class TestLightspeedRetailIntegration:
    """Integration tests for Lightspeed Retail Agent"""

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