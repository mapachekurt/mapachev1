"""Tests for Orchestrator Agent."""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import OrchestratorAgent


@pytest.fixture
def agent():
    """Create orchestrator agent instance."""
    return OrchestratorAgent()


@pytest.fixture
def mock_validation_result():
    """Mock validation result."""
    return {
        "validation_score": 75,
        "evidence": {
            "mention_count": 50,
            "frustration_score": 80,
            "urgency_score": 70,
            "top_quotes": ["Quote 1", "Quote 2"],
            "competitor_weaknesses": {}
        },
        "recommendation": "STRONG VALIDATION"
    }


@pytest.fixture
def mock_opportunity_result():
    """Mock opportunity analysis result."""
    return {
        "opportunity_score": 70,
        "market_size": {
            "TAM_dollars": 500_000_000,
            "SAM_dollars": 150_000_000,
            "SOM_dollars": 10_000_000,
            "growth_rate_cagr": 0.15
        },
        "build_strategy": {
            "recommendation": "fork",
            "estimated_time_savings": "3 months",
            "estimated_cost_savings": "$50,000"
        },
        "strategic_recommendation": "STRONG OPPORTUNITY"
    }


@pytest.fixture
def mock_combined_result(mock_validation_result, mock_opportunity_result):
    """Mock combined result."""
    return {
        "input": {
            "problem": "test problem",
            "market": "test market",
            "functionality": "test functionality"
        },
        "validation": mock_validation_result,
        "opportunity": mock_opportunity_result
    }


@pytest.mark.asyncio
async def test_discover_opportunities_integration(
    agent,
    mock_validation_result,
    mock_opportunity_result
):
    """Test full discovery workflow with mocked agent calls."""
    with patch.object(agent.router, 'parallel_analysis', new_callable=AsyncMock) as mock_router:
        mock_router.return_value = [{
            "input": {
                "problem": "test problem",
                "market": "test market",
                "functionality": "test functionality"
            },
            "validation": mock_validation_result,
            "opportunity": mock_opportunity_result
        }]

        with patch.object(agent.linear, 'create_project') as mock_linear:
            mock_linear.return_value = {
                "project_id": "proj_123",
                "project_url": "https://linear.app/project/123",
                "issues": []
            }

            result = await agent.discover_opportunities([
                {
                    "problem": "test problem",
                    "market": "test market",
                    "functionality": "test functionality",
                    "subreddits": ["test"],
                    "competitors": []
                }
            ])

            assert "ranked_opportunities" in result
            assert "synthesis" in result
            assert "linear_project" in result
            assert "recommendation" in result
            assert len(result["ranked_opportunities"]) == 1


@pytest.mark.asyncio
async def test_single_opportunity_analysis(agent, mock_validation_result, mock_opportunity_result):
    """Test analyzing a single opportunity."""
    with patch.object(agent.router, 'parallel_analysis', new_callable=AsyncMock) as mock_router:
        mock_router.return_value = [{
            "input": {
                "problem": "test",
                "market": "test",
                "functionality": "test"
            },
            "validation": mock_validation_result,
            "opportunity": mock_opportunity_result
        }]

        with patch.object(agent.linear, 'create_project') as mock_linear:
            mock_linear.return_value = {"project_id": "123", "project_url": "https://test"}

            result = await agent.analyze_single_opportunity(
                problem="test",
                market="test",
                functionality="test"
            )

            assert "analysis" in result
            assert "synthesis" in result
            assert result["analysis"] is not None


def test_final_recommendation_strong(agent):
    """Test strong recommendation generation."""
    synthesis = {
        "top_recommendation": {
            "input": {"problem": "test problem"},
            "combined_score": 85,
            "validation": {"validation_score": 90},
            "opportunity": {"opportunity_score": 80}
        }
    }

    linear_project = {
        "project_url": "https://linear.app/test"
    }

    rec = agent._generate_final_recommendation(synthesis, linear_project)

    assert "STRONG RECOMMENDATION" in rec
    assert "BUILD IMMEDIATELY" in rec
    assert "85/100" in rec


def test_final_recommendation_moderate(agent):
    """Test moderate recommendation generation."""
    synthesis = {
        "top_recommendation": {
            "input": {"problem": "test problem"},
            "combined_score": 60,
            "validation": {"validation_score": 65},
            "opportunity": {"opportunity_score": 55}
        }
    }

    rec = agent._generate_final_recommendation(synthesis, None)

    assert "MODERATE RECOMMENDATION" in rec
    assert "VALIDATE FURTHER" in rec


def test_final_recommendation_weak(agent):
    """Test weak recommendation generation."""
    synthesis = {
        "top_recommendation": {
            "input": {"problem": "test problem"},
            "combined_score": 30,
            "validation": {"validation_score": 35},
            "opportunity": {"opportunity_score": 25}
        }
    }

    rec = agent._generate_final_recommendation(synthesis, None)

    assert "WEAK RECOMMENDATION" in rec or "HIGH RISK" in rec


def test_final_recommendation_none(agent):
    """Test recommendation with no opportunities."""
    synthesis = {
        "top_recommendation": None
    }

    rec = agent._generate_final_recommendation(synthesis, None)

    assert "NO VIABLE OPPORTUNITIES" in rec


@pytest.mark.asyncio
async def test_linear_project_not_created_low_score(agent, mock_validation_result, mock_opportunity_result):
    """Test that Linear project is not created for low scores."""
    # Make scores low
    mock_validation_result["validation_score"] = 20
    mock_opportunity_result["opportunity_score"] = 25

    with patch.object(agent.router, 'parallel_analysis', new_callable=AsyncMock) as mock_router:
        mock_router.return_value = [{
            "input": {"problem": "test", "market": "test", "functionality": "test"},
            "validation": mock_validation_result,
            "opportunity": mock_opportunity_result
        }]

        with patch.object(agent.linear, 'create_project') as mock_linear:
            result = await agent.discover_opportunities([
                {"problem": "test", "market": "test", "functionality": "test"}
            ])

            # Combined score should be below 50
            assert result["ranked_opportunities"][0]["combined_score"] < 50
            # Linear project should not be created
            assert result["linear_project"] is None
            # create_project should not have been called
            mock_linear.assert_not_called()
