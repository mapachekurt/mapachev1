"""
Tests for HashiCorp Vault Agent
"""

import pytest
from agents.saas_agents.vault.agent import VaultAgent, vault_agent


class TestVaultAgent:
    """Test suite for HashiCorp Vault Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = VaultAgent()
        assert agent.agent_id == "agent_698"
        assert agent.role == "HashiCorp Vault Specialist"
        assert agent.tier == "Developer Tools"
        assert agent.category == "devops"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = VaultAgent()
        result = agent.execute("test task")
        assert "HashiCorp Vault Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = VaultAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = VaultAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_698"
        assert config["tier"] == "Developer Tools"
        assert config["category"] == "devops"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert vault_agent.agent_id == "agent_698"


class TestVaultIntegration:
    """Integration tests for HashiCorp Vault Agent"""

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