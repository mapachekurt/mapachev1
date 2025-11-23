"""Tests for Opportunity Agent."""
import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import OpportunityAgent


@pytest.fixture
def agent():
    """Create an opportunity agent instance."""
    return OpportunityAgent()


@pytest.fixture
def mock_market_data():
    """Mock market size data."""
    return {
        "TAM_dollars": 500_000_000,
        "SAM_dollars": 150_000_000,
        "SOM_dollars": 10_000_000,
        "growth_rate_cagr": 0.15,
        "market_drivers": ["Driver 1", "Driver 2"],
        "sources": ["Source 1"],
        "analysis_notes": "Test notes"
    }


@pytest.fixture
def mock_oss_options():
    """Mock OSS project options."""
    return [
        {
            "name": "test-project",
            "stars": 1500,
            "fork_score": 85,
            "license": "MIT",
            "days_since_push": 10,
            "fork_recommendation": "🟢 Excellent fork candidate"
        },
        {
            "name": "another-project",
            "stars": 500,
            "fork_score": 60,
            "license": "Apache-2.0",
            "days_since_push": 30,
            "fork_recommendation": "🟡 Good fork candidate"
        }
    ]


def test_opportunity_score_calculation_high_market(agent, mock_market_data, mock_oss_options):
    """Test opportunity score with large market."""
    score = agent._calculate_opportunity_score(
        market=mock_market_data,
        competitors={
            "average_rating": 3.2,
            "competitors": [{"name": "Comp1"}, {"name": "Comp2"}]
        },
        oss=mock_oss_options
    )

    assert 0 <= score <= 100
    assert score >= 70  # Should be high with good signals


def test_opportunity_score_small_market(agent):
    """Test opportunity score with small market."""
    score = agent._calculate_opportunity_score(
        market={"TAM_dollars": 100_000, "growth_rate_cagr": 0.02},
        competitors={},
        oss=[]
    )

    assert score < 40  # Should be low


def test_strategy_generation_strong(agent):
    """Test strong opportunity strategy."""
    strategy = agent._generate_strategy(
        80,
        {"recommendation": "fork"}
    )

    assert "STRONG OPPORTUNITY" in strategy
    assert "FORK" in strategy


def test_strategy_generation_weak(agent):
    """Test weak opportunity strategy."""
    strategy = agent._generate_strategy(
        15,
        {"recommendation": "build"}
    )

    assert "WEAK OPPORTUNITY" in strategy


@patch('tools.market_analyzer.MarketAnalyzer.calculate_tam_sam_som')
@patch('tools.market_analyzer.MarketAnalyzer.analyze_market_trends')
@patch('tools.oss_finder.OSSFinder.find_relevant_projects')
@patch('tools.build_fork_advisor.BuildForkAdvisor.recommend')
def test_analyze_opportunity_integration(
    mock_advisor,
    mock_oss,
    mock_trends,
    mock_market,
    agent,
    mock_market_data,
    mock_oss_options
):
    """Test full opportunity analysis flow."""
    mock_market.return_value = mock_market_data
    mock_trends.return_value = {"trends": [{"name": "Trend 1"}]}
    mock_oss.return_value = mock_oss_options
    mock_advisor.return_value = {
        "recommendation": "fork",
        "selected_project": mock_oss_options[0],
        "estimated_time_savings": "3 months",
        "estimated_cost_savings": "$50,000",
        "risks": ["Risk 1"]
    }

    result = agent.analyze_opportunity(
        market_segment="test market",
        functionality="test functionality",
        competitors=["Comp1"],
        preferred_language="Python"
    )

    assert "opportunity_score" in result
    assert "market_size" in result
    assert "build_strategy" in result
    assert "strategic_recommendation" in result
    assert result["opportunity_score"] >= 0
    assert result["opportunity_score"] <= 100


def test_no_oss_options(agent, mock_market_data):
    """Test analysis with no OSS options found."""
    with patch.object(agent.market, 'calculate_tam_sam_som') as mock_market:
        mock_market.return_value = mock_market_data

        with patch.object(agent.market, 'analyze_market_trends') as mock_trends:
            mock_trends.return_value = {"trends": []}

            with patch.object(agent.oss, 'find_relevant_projects') as mock_oss:
                mock_oss.return_value = []

                with patch.object(agent.advisor, 'recommend') as mock_advisor:
                    mock_advisor.return_value = {
                        "recommendation": "build",
                        "rationale": "No OSS options",
                        "estimated_time_savings": "N/A"
                    }

                    result = agent.analyze_opportunity(
                        market_segment="test",
                        functionality="test"
                    )

                    assert result["build_strategy"]["recommendation"] == "build"
                    assert result["oss_recommendations"] == []


def test_high_growth_market_bonus(agent):
    """Test that high growth markets get bonus points."""
    high_growth_score = agent._calculate_opportunity_score(
        market={"TAM_dollars": 50_000_000, "growth_rate_cagr": 0.25},
        competitors={},
        oss=[]
    )

    low_growth_score = agent._calculate_opportunity_score(
        market={"TAM_dollars": 50_000_000, "growth_rate_cagr": 0.02},
        competitors={},
        oss=[]
    )

    assert high_growth_score > low_growth_score
