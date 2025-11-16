"""
Tests for RapidMiner Agent
"""

import pytest
from agents.saas_agents.rapidminer.agent import RapidminerAgent, rapidminer_agent


class TestRapidminerAgent:
    """Test suite for RapidMiner Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = RapidminerAgent()
        assert agent.agent_id == "agent_1415"
        assert agent.role == "RapidMiner Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ml"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = RapidminerAgent()
        result = agent.execute("test task")
        assert "RapidMiner Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = RapidminerAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = RapidminerAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1415"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ml"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rapidminer_agent.agent_id == "agent_1415"


class TestRapidminerIntegration:
    """Integration tests for RapidMiner Agent"""

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