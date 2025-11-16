"""
Tests for Duo Security Agent
"""

import pytest
from agents.saas_agents.duo_security.agent import DuoSecurityAgent, duo_security_agent


class TestDuoSecurityAgent:
    """Test suite for Duo Security Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DuoSecurityAgent()
        assert agent.agent_id == "agent_1435"
        assert agent.role == "Duo Security Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DuoSecurityAgent()
        result = agent.execute("test task")
        assert "Duo Security Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DuoSecurityAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DuoSecurityAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1435"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert duo_security_agent.agent_id == "agent_1435"


class TestDuoSecurityIntegration:
    """Integration tests for Duo Security Agent"""

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