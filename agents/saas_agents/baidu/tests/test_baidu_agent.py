"""
Tests for Baidu Agent
"""

import pytest
from agents.saas_agents.baidu.agent import BaiduAgent, baidu_agent


class TestBaiduAgent:
    """Test suite for Baidu Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = BaiduAgent()
        assert agent.agent_id == "agent_1490"
        assert agent.role == "Baidu Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = BaiduAgent()
        result = agent.execute("test task")
        assert "Baidu Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = BaiduAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = BaiduAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1490"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert baidu_agent.agent_id == "agent_1490"


class TestBaiduIntegration:
    """Integration tests for Baidu Agent"""

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