"""
Tests for Terraform Agent
"""

import pytest
from agents.saas_agents.terraform.agent import TerraformAgent, terraform_agent


class TestTerraformAgent:
    """Test suite for Terraform Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = TerraformAgent()
        assert agent.agent_id == "agent_687"
        assert agent.role == "Terraform Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = TerraformAgent()
        result = agent.execute("test task")
        assert "Terraform Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = TerraformAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = TerraformAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_687"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert terraform_agent.agent_id == "agent_687"


class TestTerraformIntegration:
    """Integration tests for Terraform Agent"""

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