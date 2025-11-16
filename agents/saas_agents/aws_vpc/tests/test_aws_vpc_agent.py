"""
Tests for AWS VPC Agent
"""

import pytest
from agents.saas_agents.aws_vpc.agent import AwsVpcAgent, aws_vpc_agent


class TestAwsVpcAgent:
    """Test suite for AWS VPC Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = AwsVpcAgent()
        assert agent.agent_id == "agent_644"
        assert agent.role == "AWS VPC Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = AwsVpcAgent()
        result = agent.execute("test task")
        assert "AWS VPC Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = AwsVpcAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = AwsVpcAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_644"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert aws_vpc_agent.agent_id == "agent_644"


class TestAwsVpcIntegration:
    """Integration tests for AWS VPC Agent"""

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