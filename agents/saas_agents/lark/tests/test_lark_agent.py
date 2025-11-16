"""
Tests for Lark (Feishu) Agent
"""

import pytest
from agents.saas_agents.lark.agent import LarkAgent, lark_agent


class TestLarkAgent:
    """Test suite for Lark (Feishu) Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = LarkAgent()
        assert agent.agent_id == "agent_1474"
        assert agent.role == "Lark (Feishu) Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = LarkAgent()
        result = agent.execute("test task")
        assert "Lark (Feishu) Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = LarkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = LarkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1474"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert lark_agent.agent_id == "agent_1474"


class TestLarkIntegration:
    """Integration tests for Lark (Feishu) Agent"""

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