"""
Tests for Square Appointments Agent
"""

import pytest
from agents.saas_agents.square_appointments.agent import SquareAppointmentsAgent, square_appointments_agent


class TestSquareAppointmentsAgent:
    """Test suite for Square Appointments Agent"""

    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = SquareAppointmentsAgent()
        assert agent.agent_id == "agent_1210"
        assert agent.role == "Square Appointments Specialist"
        assert agent.tier == "Specialized Vertical Tools"
        assert agent.category == "booking"

    def test_agent_execute(self):
        """Test agent execute method"""
        agent = SquareAppointmentsAgent()
        result = agent.execute("test task")
        assert "Square Appointments Agent executing" in result
        assert "test task" in result

    def test_agent_capabilities(self):
        """Test agent capabilities"""
        agent = SquareAppointmentsAgent()
        capabilities = agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
        assert "API Operations" in capabilities

    def test_agent_config(self):
        """Test agent configuration"""
        agent = SquareAppointmentsAgent()
        config = agent.get_config()
        assert config["agent_id"] == "agent_1210"
        assert config["tier"] == "Specialized Vertical Tools"
        assert config["category"] == "booking"

    def test_singleton_instance(self):
        """Test singleton agent instance"""
        assert square_appointments_agent.agent_id == "agent_1210"


class TestSquareAppointmentsIntegration:
    """Integration tests for Square Appointments Agent"""

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