"""
Tests for Kakao Work Agent
"""

import pytest
from agents.saas_agents.kakao_work.agent import KakaoWorkAgent, kakao_work_agent


class TestKakaoWorkAgent:
    """Test suite for Kakao Work Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = KakaoWorkAgent()
        assert agent.agent_id == "agent_1475"
        assert agent.role == "Kakao Work Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "regional"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = KakaoWorkAgent()
        result = agent.execute("test task")
        assert "Kakao Work Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = KakaoWorkAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = KakaoWorkAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1475"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "regional"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert kakao_work_agent.agent_id == "agent_1475"


class TestKakaoWorkIntegration:
    """Integration tests for Kakao Work Agent"""

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