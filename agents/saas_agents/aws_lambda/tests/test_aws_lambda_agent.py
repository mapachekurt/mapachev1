"""
Tests for AWS Lambda Agent
"""

import pytest
from agents.saas_agents.aws_lambda.agent import AwsLambdaAgent, aws_lambda_agent


class TestAwsLambdaAgent:
    """Test suite for AWS Lambda Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AwsLambdaAgent()
        assert agent.agent_id == "agent_639"
        assert agent.role == "AWS Lambda Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AwsLambdaAgent()
        result = agent.execute("test task")
        assert "AWS Lambda Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AwsLambdaAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AwsLambdaAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_639"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aws_lambda_agent.agent_id == "agent_639"


class TestAwsLambdaIntegration:
    """Integration tests for AWS Lambda Agent"""

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