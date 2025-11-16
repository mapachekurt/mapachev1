"""
Tests for Rapid7 Agent
"""

import pytest
from agents.saas_agents.rapid7.agent import Rapid7Agent, rapid7_agent


class TestRapid7Agent:
    """Test suite for Rapid7 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = Rapid7Agent()
        assert agent.agent_id == "agent_1437"
        assert agent.role == "Rapid7 Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = Rapid7Agent()
        result = agent.execute("test task")
        assert "Rapid7 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = Rapid7Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = Rapid7Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1437"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert rapid7_agent.agent_id == "agent_1437"


class TestRapid7Integration:
    """Integration tests for Rapid7 Agent"""

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