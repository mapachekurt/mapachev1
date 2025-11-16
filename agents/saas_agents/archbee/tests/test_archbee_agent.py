"""
Tests for Archbee Agent
"""

import pytest
from agents.saas_agents.archbee.agent import ArchbeeAgent, archbee_agent


class TestArchbeeAgent:
    """Test suite for Archbee Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ArchbeeAgent()
        assert agent.agent_id == "agent_782"
        assert agent.role == "Archbee Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ArchbeeAgent()
        result = agent.execute("test task")
        assert "Archbee Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ArchbeeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ArchbeeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_782"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert archbee_agent.agent_id == "agent_782"


class TestArchbeeIntegration:
    """Integration tests for Archbee Agent"""

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