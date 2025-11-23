"""Reddit scraping with PRAW integration."""
import os
import praw
from typing import List, Dict
from datetime import datetime, timedelta


class RedditScraper:
    """Scrape Reddit for pain point mentions and discussions."""

    def __init__(self):
        """Initialize Reddit API client."""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="ValidationAgent/1.0"
        )

    def search_pain_points(
        self,
        query: str,
        subreddits: List[str],
        timeframe: str = "week"
    ) -> Dict:
        """
        Search Reddit for pain point mentions.

        Args:
            query: Search term (e.g., "equipment tracking")
            subreddits: List of subreddits (e.g., ["construction", "contractors"])
            timeframe: week, month, year

        Returns:
            {
                "mentions": int,
                "posts": List[Post],
                "sentiment_summary": Dict,
                "top_quotes": List[str]
            }
        """
        mentions = []

        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)

                # Search posts
                for submission in subreddit.search(query, time_filter=timeframe, limit=100):
                    mentions.append({
                        "type": "post",
                        "text": f"{submission.title}\n{submission.selftext}",
                        "score": submission.score,
                        "url": f"https://reddit.com{submission.permalink}",
                        "created": datetime.fromtimestamp(submission.created_utc).isoformat(),
                        "author": str(submission.author),
                        "subreddit": subreddit_name
                    })

                    # Analyze top comments
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list()[:20]:
                        if len(comment.body) > 50:
                            mentions.append({
                                "type": "comment",
                                "text": comment.body,
                                "score": comment.score,
                                "url": f"https://reddit.com{comment.permalink}",
                                "created": datetime.fromtimestamp(comment.created_utc).isoformat(),
                                "subreddit": subreddit_name
                            })
            except Exception as e:
                print(f"Error scraping r/{subreddit_name}: {e}")
                continue

        return {
            "mentions": len(mentions),
            "posts": mentions,
            "timeframe": timeframe,
            "subreddits": subreddits
        }

    def get_trending_topics(self, subreddits: List[str], limit: int = 10) -> List[Dict]:
        """Get trending topics from specified subreddits."""
        trending = []

        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                for submission in subreddit.hot(limit=limit):
                    trending.append({
                        "title": submission.title,
                        "score": submission.score,
                        "comments": submission.num_comments,
                        "url": f"https://reddit.com{submission.permalink}",
                        "subreddit": subreddit_name
                    })
            except Exception as e:
                print(f"Error getting trending from r/{subreddit_name}: {e}")
                continue

        # Sort by engagement (score + comments)
        trending.sort(key=lambda x: x["score"] + x["comments"], reverse=True)
        return trending[:limit]
