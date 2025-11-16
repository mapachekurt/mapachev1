"""
Tests for Gorgias Agent
"""

import pytest
from agents.saas_agents.gorgias.agent import GorgiasAgent, gorgias_agent


class TestGorgiasAgent:
    """Test suite for Gorgias Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GorgiasAgent()
        assert agent.agent_id == "agent_1005"
        assert agent.role == "Gorgias Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "support"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GorgiasAgent()
        result = agent.execute("test task")
        assert "Gorgias Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GorgiasAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GorgiasAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1005"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "support"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gorgias_agent.agent_id == "agent_1005"


class TestGorgiasIntegration:
    """Integration tests for Gorgias Agent"""

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