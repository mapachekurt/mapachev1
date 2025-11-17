"""
Tests for Agent Registry Service
"""

import pytest
from fastapi.testclient import TestClient

from infrastructure.registry.main import app, AGENTS_DB, load_agent_cards


@pytest.fixture
def client():
    """Test client for the registry service"""
    return TestClient(app)


@pytest.fixture
def auth_headers(bearer_token):
    """Authentication headers"""
    return {"Authorization": f"Bearer {bearer_token}"}


def test_root_endpoint(client):
    """Test the root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "A2A Agent Registry"


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_agents_requires_auth(client):
    """Test that listing agents requires authentication"""
    response = client.get("/agents")
    assert response.status_code == 403  # Forbidden without auth


def test_list_agents_with_auth(client, auth_headers):
    """Test listing agents with authentication"""
    response = client.get("/agents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert "total" in data
    assert isinstance(data["agents"], list)


def test_get_agent_by_name(client, auth_headers):
    """Test getting a specific agent by name"""
    # First, we need to have some agents in the database
    # In a real test, we'd populate the test database
    # For now, we'll test the error case
    response = client.get("/agents/nonexistent", headers=auth_headers)
    assert response.status_code == 404


def test_search_agents(client, auth_headers):
    """Test searching for agents"""
    search_payload = {
        "skill": "software_engineering",
        "department": "engineering",
    }

    response = client.post("/agents/search", headers=auth_headers, json=search_payload)
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert "total" in data


def test_register_agent(client, auth_headers):
    """Test registering a new agent"""
    agent_payload = {
        "name": "test_new_agent",
        "description": "A test agent",
        "version": "1.0.0",
        "capabilities": {
            "skills": ["test_skill"],
            "tools": ["test_tool"],
            "model": "gemini-2.0-flash-exp",
        },
        "metadata": {
            "role": "Test Role",
            "department": "test",
            "reports_to": None,
            "manages": [],
            "tags": ["test"],
        },
        "authentication": {
            "type": "bearer",
            "required": True,
        },
        "contact": {
            "email": "test@example.com",
        },
    }

    response = client.post("/agents/register", headers=auth_headers, json=agent_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "agent" in data


def test_search_by_department(client, auth_headers):
    """Test filtering agents by department"""
    response = client.get("/agents?department=engineering", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
