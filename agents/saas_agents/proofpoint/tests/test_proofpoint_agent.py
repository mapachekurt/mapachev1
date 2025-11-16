"""
Tests for Proofpoint Agent
"""

import pytest
from agents.saas_agents.proofpoint.agent import ProofpointAgent, proofpoint_agent


class TestProofpointAgent:
    """Test suite for Proofpoint Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = ProofpointAgent()
        assert agent.agent_id == "agent_1443"
        assert agent.role == "Proofpoint Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "security"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = ProofpointAgent()
        result = agent.execute("test task")
        assert "Proofpoint Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = ProofpointAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = ProofpointAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1443"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "security"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert proofpoint_agent.agent_id == "agent_1443"


class TestProofpointIntegration:
    """Integration tests for Proofpoint Agent"""

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