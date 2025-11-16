"""
Tests for CrowdStrike Agent
"""

import pytest
from agents.saas_agents.crowdstrike.agent import CrowdstrikeAgent, crowdstrike_agent


class TestCrowdstrikeAgent:
    """Test suite for CrowdStrike Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = CrowdstrikeAgent()
        assert agent.agent_id == "agent_1439"
        assert agent.role == "CrowdStrike Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = CrowdstrikeAgent()
        result = agent.execute("test task")
        assert "CrowdStrike Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = CrowdstrikeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = CrowdstrikeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1439"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert crowdstrike_agent.agent_id == "agent_1439"


class TestCrowdstrikeIntegration:
    """Integration tests for CrowdStrike Agent"""

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