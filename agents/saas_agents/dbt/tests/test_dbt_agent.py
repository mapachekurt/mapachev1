"""
Tests for dbt (Data Build Tool) Agent
"""

import pytest
from agents.saas_agents.dbt.agent import DbtAgent, dbt_agent


class TestDbtAgent:
    """Test suite for dbt (Data Build Tool) Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DbtAgent()
        assert agent.agent_id == "agent_1384"
        assert agent.role == "dbt (Data Build Tool) Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "data"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = DbtAgent()
        result = agent.execute("test task")
        assert "dbt (Data Build Tool) Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = DbtAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = DbtAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1384"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "data"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert dbt_agent.agent_id == "agent_1384"


class TestDbtIntegration:
    """Integration tests for dbt (Data Build Tool) Agent"""

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