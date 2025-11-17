"""
Tests for BaseA2AAgent
"""

import json
import pytest
from pathlib import Path

from agents.core import BaseA2AAgent, AgentConfig


def test_agent_initialization(sample_agent_config):
    """Test that agent initializes correctly"""
    agent = BaseA2AAgent(sample_agent_config)

    assert agent.config.name == "test_agent"
    assert agent.config.department == "test_department"
    assert len(agent.config.skills) == 3
    assert agent._adk_agent is not None
    assert agent._agent_card is not None


def test_agent_card_generation(sample_agent_config):
    """Test agent card generation"""
    agent = BaseA2AAgent(sample_agent_config)
    agent_card = agent.get_agent_card()

    assert agent_card["name"] == "test_agent"
    assert agent_card["description"] == sample_agent_config.description
    assert "capabilities" in agent_card
    assert "metadata" in agent_card
    assert "authentication" in agent_card
    assert agent_card["capabilities"]["skills"] == sample_agent_config.skills


def test_agent_card_save(sample_agent_config, test_agent_cards_dir):
    """Test saving agent card to disk"""
    agent = BaseA2AAgent(sample_agent_config)
    filepath = agent.save_agent_card(test_agent_cards_dir)

    assert Path(filepath).exists()
    assert Path(filepath).name == "test_agent.json"

    # Verify content
    with open(filepath, 'r') as f:
        saved_card = json.load(f)

    assert saved_card["name"] == "test_agent"


def test_agent_hierarchy(sample_agent_config):
    """Test agent hierarchy (reports_to, manages)"""
    agent = BaseA2AAgent(sample_agent_config)
    agent_card = agent.get_agent_card()

    assert agent_card["metadata"]["reports_to"] == "test_manager"
    assert len(agent_card["metadata"]["manages"]) == 2
    assert "test_report_1" in agent_card["metadata"]["manages"]


def test_add_sub_agent(sample_agent_config):
    """Test adding sub-agents"""
    manager_config = AgentConfig(
        name="manager_agent",
        description="Manager agent",
        role="Manager",
        department="test_department",
        skills=["management"],
        manages=["test_agent"],
    )

    manager = BaseA2AAgent(manager_config)
    sub_agent = BaseA2AAgent(sample_agent_config)

    manager.add_sub_agent(sub_agent)

    assert manager._adk_agent.sub_agents is not None
    assert len(manager._adk_agent.sub_agents) > 0
