"""
Tests for ReadMe Agent
"""

import pytest
from agents.saas_agents.readme.agent import ReadmeAgent, readme_agent


class TestReadmeAgent:
    """Test suite for ReadMe Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ReadmeAgent()
        assert agent.agent_id == "agent_773"
        assert agent.role == "ReadMe Specialist"
        assert agent.tier == "Productivity & Collaboration"
        assert agent.category == "documentation"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ReadmeAgent()
        result = agent.execute("test task")
        assert "ReadMe Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ReadmeAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ReadmeAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_773"
        assert config["tier"] == "Productivity & Collaboration"
        assert config["category"] == "documentation"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert readme_agent.agent_id == "agent_773"


class TestReadmeIntegration:
    """Integration tests for ReadMe Agent"""

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