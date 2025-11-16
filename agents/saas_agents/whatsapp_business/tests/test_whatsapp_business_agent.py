"""
Tests for WhatsApp Business Agent
"""

import pytest
from agents.saas_agents.whatsapp_business.agent import WhatsappBusinessAgent, whatsapp_business_agent


class TestWhatsappBusinessAgent:
    """Test suite for WhatsApp Business Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = WhatsappBusinessAgent()
        assert agent.agent_id == "agent_834"
        assert agent.role == "WhatsApp Business Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "communication"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = WhatsappBusinessAgent()
        result = agent.execute("test task")
        assert "WhatsApp Business Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = WhatsappBusinessAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = WhatsappBusinessAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_834"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "communication"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert whatsapp_business_agent.agent_id == "agent_834"


class TestWhatsappBusinessIntegration:
    """Integration tests for WhatsApp Business Agent"""

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