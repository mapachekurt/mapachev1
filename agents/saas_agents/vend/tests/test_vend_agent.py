"""
Tests for Vend (Lightspeed Retail) Agent
"""

import pytest
from agents.saas_agents.vend.agent import VendAgent, vend_agent


class TestVendAgent:
    """Test suite for Vend (Lightspeed Retail) Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VendAgent()
        assert agent.agent_id == "agent_1172"
        assert agent.role == "Vend (Lightspeed Retail) Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "retail"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VendAgent()
        result = agent.execute("test task")
        assert "Vend (Lightspeed Retail) Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VendAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VendAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1172"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "retail"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert vend_agent.agent_id == "agent_1172"


class TestVendIntegration:
    """Integration tests for Vend (Lightspeed Retail) Agent"""

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