"""
Tests for Endicia Agent
"""

import pytest
from agents.saas_agents.endicia.agent import EndiciaAgent, endicia_agent


class TestEndiciaAgent:
    """Test suite for Endicia Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = EndiciaAgent()
        assert agent.agent_id == "agent_1118"
        assert agent.role == "Endicia Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "logistics"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = EndiciaAgent()
        result = agent.execute("test task")
        assert "Endicia Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = EndiciaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = EndiciaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1118"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "logistics"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert endicia_agent.agent_id == "agent_1118"


class TestEndiciaIntegration:
    """Integration tests for Endicia Agent"""

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