"""
Tests for Hugging Face Agent
"""

import pytest
from agents.saas_agents.huggingface.agent import HuggingfaceAgent, huggingface_agent


class TestHuggingfaceAgent:
    """Test suite for Hugging Face Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = HuggingfaceAgent()
        assert agent.agent_id == "agent_1455"
        assert agent.role == "Hugging Face Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "ai"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = HuggingfaceAgent()
        result = agent.execute("test task")
        assert "Hugging Face Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = HuggingfaceAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = HuggingfaceAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1455"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "ai"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert huggingface_agent.agent_id == "agent_1455"


class TestHuggingfaceIntegration:
    """Integration tests for Hugging Face Agent"""

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