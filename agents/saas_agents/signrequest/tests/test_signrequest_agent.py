"""
Tests for SignRequest Agent
"""

import pytest
from agents.saas_agents.signrequest.agent import SignrequestAgent, signrequest_agent


class TestSignrequestAgent:
    """Test suite for SignRequest Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SignrequestAgent()
        assert agent.agent_id == "agent_1322"
        assert agent.role == "SignRequest Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "utility"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SignrequestAgent()
        result = agent.execute("test task")
        assert "SignRequest Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SignrequestAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SignrequestAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1322"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "utility"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert signrequest_agent.agent_id == "agent_1322"


class TestSignrequestIntegration:
    """Integration tests for SignRequest Agent"""

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