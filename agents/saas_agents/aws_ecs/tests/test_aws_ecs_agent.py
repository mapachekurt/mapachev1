"""
Tests for AWS ECS Agent
"""

import pytest
from agents.saas_agents.aws_ecs.agent import AwsEcsAgent, aws_ecs_agent


class TestAwsEcsAgent:
    """Test suite for AWS ECS Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AwsEcsAgent()
        assert agent.agent_id == "agent_646"
        assert agent.role == "AWS ECS Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AwsEcsAgent()
        result = agent.execute("test task")
        assert "AWS ECS Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AwsEcsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AwsEcsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_646"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aws_ecs_agent.agent_id == "agent_646"


class TestAwsEcsIntegration:
    """Integration tests for AWS ECS Agent"""

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