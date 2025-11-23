"""
Pytest configuration and fixtures
"""

import pytest
import os
from pathlib import Path


@pytest.fixture
def test_agent_cards_dir(tmp_path):
    """Create a temporary directory for test agent cards"""
    cards_dir = tmp_path / "test_agent_cards"
    cards_dir.mkdir()
    return str(cards_dir)


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing"""
    from agents.core import AgentConfig

    return AgentConfig(
        name="test_agent",
        description="Test agent for unit tests",
        role="Test Role",
        department="test_department",
        skills=["skill1", "skill2", "skill3"],
        tools=["tool1", "tool2"],
        reports_to="test_manager",
        manages=["test_report_1", "test_report_2"],
    )


@pytest.fixture
def bearer_token():
    """Test bearer token"""
    return "test-token-12345"


@pytest.fixture(autouse=True)
def set_test_env(bearer_token):
    """Set test environment variables"""
    os.environ["BEARER_TOKEN"] = bearer_token
    os.environ["A2A_REGISTRY_URL"] = "http://localhost:8080"
    os.environ["USE_IN_MEMORY_DB"] = "true"
    os.environ["ENVIRONMENT"] = "test"
