"""Twitter/X API integration for sentiment analysis."""
import os
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class TwitterAPI:
    """Search X/Twitter for mentions and sentiment."""

    def __init__(self):
        """Initialize Twitter API client."""
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }

    def search_mentions(
        self,
        query: str,
        max_results: int = 100,
        days_back: int = 7
    ) -> Dict:
        """
        Search Twitter for mentions of a topic.

        Args:
            query: Search query (supports Twitter search operators)
            max_results: Maximum results (10-100)
            days_back: Number of days to search back

        Returns:
            {
                "mention_count": int,
                "tweets": List[Dict],
                "engagement_total": int
            }
        """
        # Calculate start time
        start_time = (datetime.now() - timedelta(days=days_back)).isoformat() + "Z"

        params = {
            "query": query,
            "max_results": min(max_results, 100),
            "start_time": start_time,
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "username,name"
        }

        try:
            response = requests.get(
                f"{self.base_url}/tweets/search/recent",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            tweets = []
            users = {user["id"]: user for user in data.get("includes", {}).get("users", [])}

            for tweet in data.get("data", []):
                author = users.get(tweet["author_id"], {})
                tweets.append({
                    "text": tweet["text"],
                    "created_at": tweet["created_at"],
                    "author": author.get("username", "unknown"),
                    "likes": tweet["public_metrics"]["like_count"],
                    "retweets": tweet["public_metrics"]["retweet_count"],
                    "replies": tweet["public_metrics"]["reply_count"],
                    "url": f"https://twitter.com/{author.get('username', 'i')}/status/{tweet['id']}"
                })

            engagement_total = sum(
                t["likes"] + t["retweets"] + t["replies"] for t in tweets
            )

            return {
                "mention_count": len(tweets),
                "tweets": tweets,
                "engagement_total": engagement_total,
                "query": query
            }

        except Exception as e:
            print(f"Error searching Twitter: {e}")
            return {
                "mention_count": 0,
                "tweets": [],
                "engagement_total": 0,
                "error": str(e)
            }

    def analyze_sentiment_patterns(self, tweets: List[Dict]) -> Dict:
        """Analyze sentiment patterns in tweets."""
        if not tweets:
            return {"negative": 0, "neutral": 0, "positive": 0}

        # Simple keyword-based sentiment (could be enhanced with ML)
        negative_keywords = ["hate", "terrible", "awful", "worst", "frustrated", "annoying"]
        positive_keywords = ["love", "great", "awesome", "best", "amazing", "perfect"]

        sentiment_counts = {"negative": 0, "neutral": 0, "positive": 0}

        for tweet in tweets:
            text_lower = tweet["text"].lower()

            negative_score = sum(1 for kw in negative_keywords if kw in text_lower)
            positive_score = sum(1 for kw in positive_keywords if kw in text_lower)

            if negative_score > positive_score:
                sentiment_counts["negative"] += 1
            elif positive_score > negative_score:
                sentiment_counts["positive"] += 1
            else:
                sentiment_counts["neutral"] += 1

        return sentiment_counts
