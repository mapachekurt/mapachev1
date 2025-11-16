"""
Tests for Snyk Agent
"""

import pytest
from agents.saas_agents.snyk.agent import SnykAgent, snyk_agent


class TestSnykAgent:
    """Test suite for Snyk Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SnykAgent()
        assert agent.agent_id == "agent_716"
        assert agent.role == "Snyk Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "code_quality"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SnykAgent()
        result = agent.execute("test task")
        assert "Snyk Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SnykAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SnykAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_716"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "code_quality"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert snyk_agent.agent_id == "agent_716"


class TestSnykIntegration:
    """Integration tests for Snyk Agent"""

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