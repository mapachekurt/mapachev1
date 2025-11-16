"""
Tests for GCP VPC Agent
"""

import pytest
from agents.saas_agents.gcp_vpc.agent import GcpVpcAgent, gcp_vpc_agent


class TestGcpVpcAgent:
    """Test suite for GCP VPC Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = GcpVpcAgent()
        assert agent.agent_id == "agent_669"
        assert agent.role == "GCP VPC Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "cloud"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = GcpVpcAgent()
        result = agent.execute("test task")
        assert "GCP VPC Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = GcpVpcAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = GcpVpcAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_669"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "cloud"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert gcp_vpc_agent.agent_id == "agent_669"


class TestGcpVpcIntegration:
    """Integration tests for GCP VPC Agent"""

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