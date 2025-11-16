"""
Tests for AWS EC2 Agent
"""

import pytest
from agents.saas_agents.aws_ec2.agent import AwsEc2Agent, aws_ec2_agent


class TestAwsEc2Agent:
    """Test suite for AWS EC2 Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AwsEc2Agent()
        assert agent.agent_id == "agent_637"
        assert agent.role == "AWS EC2 Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AwsEc2Agent()
        result = agent.execute("test task")
        assert "AWS EC2 Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AwsEc2Agent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AwsEc2Agent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_637"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aws_ec2_agent.agent_id == "agent_637"


class TestAwsEc2Integration:
    """Integration tests for AWS EC2 Agent"""

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