"""
Tests for Globalization Partners Agent
"""

import pytest
from agents.saas_agents.globalization_partners.agent import GlobalizationPartnersAgent, globalization_partners_agent


class TestGlobalizationPartnersAgent:
    """Test suite for Globalization Partners Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GlobalizationPartnersAgent()
        assert agent.agent_id == "agent_965"
        assert agent.role == "Globalization Partners Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "hr"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GlobalizationPartnersAgent()
        result = agent.execute("test task")
        assert "Globalization Partners Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GlobalizationPartnersAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GlobalizationPartnersAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_965"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "hr"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert globalization_partners_agent.agent_id == "agent_965"


class TestGlobalizationPartnersIntegration:
    """Integration tests for Globalization Partners Agent"""

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