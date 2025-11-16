"""
Tests for AWS IAM Agent
"""

import pytest
from agents.saas_agents.aws_iam.agent import AwsIamAgent, aws_iam_agent


class TestAwsIamAgent:
    """Test suite for AWS IAM Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AwsIamAgent()
        assert agent.agent_id == "agent_645"
        assert agent.role == "AWS IAM Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AwsIamAgent()
        result = agent.execute("test task")
        assert "AWS IAM Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AwsIamAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AwsIamAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_645"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aws_iam_agent.agent_id == "agent_645"


class TestAwsIamIntegration:
    """Integration tests for AWS IAM Agent"""

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