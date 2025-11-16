"""
Tests for HelloSign Agent
"""

import pytest
from agents.saas_agents.hellosign.agent import HellosignAgent, hellosign_agent


class TestHellosignAgent:
    """Test suite for HelloSign Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HellosignAgent()
        assert agent.agent_id == "agent_1319"
        assert agent.role == "HelloSign Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HellosignAgent()
        result = agent.execute("test task")
        assert "HelloSign Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HellosignAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HellosignAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1319"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert hellosign_agent.agent_id == "agent_1319"


class TestHellosignIntegration:
    """Integration tests for HelloSign Agent"""

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