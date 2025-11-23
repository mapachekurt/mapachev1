"""Tests for Validation Agent."""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ValidationAgent


@pytest.fixture
def agent():
    """Create a validation agent instance."""
    return ValidationAgent()


@pytest.fixture
def mock_reddit_data():
    """Mock Reddit data."""
    return {
        "mentions": 47,
        "posts": [
            {
                "type": "post",
                "text": "We waste so much time tracking equipment manually!",
                "score": 15,
                "url": "https://reddit.com/test",
                "created": "2025-01-01T00:00:00",
                "author": "testuser",
                "subreddit": "construction"
            }
        ] * 47,
        "timeframe": "week",
        "subreddits": ["construction"]
    }


@pytest.fixture
def mock_sentiment_data():
    """Mock sentiment analysis data."""
    return {
        "frustration_score": 85,
        "urgency_score": 75,
        "top_quotes": [
            "We waste 2 hours daily looking for equipment",
            "Current solutions are too expensive",
            "Nothing works offline on job sites"
        ],
        "sentiment_breakdown": {
            "very_frustrated": 25,
            "frustrated": 15,
            "mild": 5,
            "neutral": 2
        }
    }


def test_validation_score_calculation(agent, mock_reddit_data, mock_sentiment_data):
    """Test validation score calculation logic."""
    score = agent._calculate_validation_score(
        reddit=mock_reddit_data,
        twitter={"mention_count": 10},
        hackernews={"story_count": 5, "comment_count": 8},
        sentiment=mock_sentiment_data,
        competitors={"ToolTracker": {"mention_count": 15}}
    )

    assert 0 <= score <= 100
    assert score >= 70  # Should be high given strong signals


def test_recommendation_strong(agent):
    """Test strong validation recommendation."""
    rec = agent._generate_recommendation(80)
    assert "STRONG VALIDATION" in rec
    assert "Build immediately" in rec


def test_recommendation_weak(agent):
    """Test weak validation recommendation."""
    rec = agent._generate_recommendation(20)
    assert "WEAK VALIDATION" in rec


def test_recommendation_none(agent):
    """Test no validation recommendation."""
    rec = agent._generate_recommendation(5)
    assert "NO VALIDATION" in rec


@patch('tools.reddit_scraper.RedditScraper.search_pain_points')
@patch('tools.sentiment_analyzer.SentimentAnalyzer.analyze_frustration')
def test_validate_opportunity_integration(
    mock_sentiment,
    mock_reddit,
    agent,
    mock_reddit_data,
    mock_sentiment_data
):
    """Test full validation flow with mocked external calls."""
    mock_reddit.return_value = mock_reddit_data
    mock_sentiment.return_value = mock_sentiment_data

    result = agent.validate_opportunity(
        problem_hypothesis="construction equipment tracking",
        target_subreddits=["construction"],
        competitors=["ToolTracker"],
        timeframe="week"
    )

    assert "validation_score" in result
    assert "evidence" in result
    assert "recommendation" in result
    assert result["validation_score"] >= 0
    assert result["validation_score"] <= 100
    assert result["problem_hypothesis"] == "construction equipment tracking"


def test_validate_opportunity_no_competitors(agent):
    """Test validation without competitor analysis."""
    with patch.object(agent.reddit, 'search_pain_points') as mock_reddit:
        mock_reddit.return_value = {
            "mentions": 5,
            "posts": [],
            "timeframe": "week",
            "subreddits": []
        }

        with patch.object(agent.sentiment, 'analyze_frustration') as mock_sentiment:
            mock_sentiment.return_value = {
                "frustration_score": 30,
                "urgency_score": 20,
                "top_quotes": [],
                "sentiment_breakdown": {}
            }

            result = agent.validate_opportunity(
                problem_hypothesis="test problem",
                target_subreddits=["test"],
                competitors=None,
                timeframe="week"
            )

            assert result["validation_score"] < 50


def test_empty_mentions(agent):
    """Test handling of no mentions found."""
    score = agent._calculate_validation_score(
        reddit={"mentions": 0},
        twitter={"mention_count": 0},
        hackernews={"story_count": 0, "comment_count": 0},
        sentiment={"frustration_score": 0, "urgency_score": 0},
        competitors={}
    )

    assert score == 0


def test_high_mentions_low_frustration(agent):
    """Test many mentions but low frustration."""
    score = agent._calculate_validation_score(
        reddit={"mentions": 100},
        twitter={"mention_count": 50},
        hackernews={"story_count": 20, "comment_count": 30},
        sentiment={"frustration_score": 10, "urgency_score": 5},
        competitors={}
    )

    # Should have points for mentions but not frustration
    assert 30 <= score <= 50


def test_low_mentions_high_frustration(agent):
    """Test few mentions but high frustration."""
    score = agent._calculate_validation_score(
        reddit={"mentions": 3},
        twitter={"mention_count": 0},
        hackernews={"story_count": 0, "comment_count": 0},
        sentiment={"frustration_score": 95, "urgency_score": 90},
        competitors={}
    )

    # Should have points for frustration/urgency but not mentions
    assert 40 <= score <= 60
