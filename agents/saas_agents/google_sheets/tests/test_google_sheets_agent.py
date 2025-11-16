"""
Tests for Google Sheets Agent
"""

import pytest
from agents.saas_agents.google_sheets.agent import GoogleSheetsAgent, google_sheets_agent


class TestGoogleSheetsAgent:
    """Test suite for Google Sheets Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GoogleSheetsAgent()
        assert agent.agent_id == "agent_519"
        assert agent.role == "Google Sheets Specialist"
        assert agent.tier == "Enterprise Essentials"
        assert agent.category == "spreadsheet"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GoogleSheetsAgent()
        result = agent.execute("test task")
        assert "Google Sheets Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GoogleSheetsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GoogleSheetsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_519"
        assert config["tier"] == "Enterprise Essentials"
        assert config["category"] == "spreadsheet"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert google_sheets_agent.agent_id == "agent_519"


class TestGoogleSheetsIntegration:
    """Integration tests for Google Sheets Agent"""

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